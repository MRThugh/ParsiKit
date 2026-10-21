"""
Regression tests for all verified defects fixed in parsikit.text and parsikit.reshaper during Phase 02.
Each test verifies a specific bug reproduction and resolution.
"""
import unittest
import unicodedata
from parsikit.text import standardize_persian, beautify_persian_spacing, clean_text, slugify
from parsikit.reshaper import reshape_for_graphics, reshape_paragraph_for_graphics


class TestTextPhase02Regressions(unittest.TestCase):
    def test_regression_beautify_spacing_urls_and_emails_split(self):
        """
        Bug: beautify_persian_spacing previously matched any dot or colon followed by non-space,
             causing URLs like 'https://example.com' to become 'https: //example. com' and
             emails like 'kamrani.exe@gmail.com' to become 'kamrani. exe@gmail. com'.
        Fix: Avoid splitting colons inside URLs and dots inside domains, emails, and filenames.
        """
        raw_url = "آدرس وب‌سایت https://parsikit.org/docs/index.html است."
        result_url = beautify_persian_spacing(raw_url)
        self.assertIn("https://parsikit.org/docs/index.html", result_url)
        self.assertNotIn("https: //", result_url)
        self.assertNotIn(". com", result_url)

        raw_email = "با ایمیل kamrani.exe@gmail.com مکاتبه نمایید."
        result_email = beautify_persian_spacing(raw_email)
        self.assertIn("kamrani.exe@gmail.com", result_email)
        self.assertNotIn("kamrani. exe", result_email)

    def test_regression_beautify_spacing_decimal_and_time_split(self):
        """
        Bug: beautify_persian_spacing inserted a space after '.' in decimal floats ('3.14' -> '3. 14')
             and after ':' in timestamps ('12:30' -> '12: 30').
        Fix: Punctuation spacing checks digit boundaries and excludes decimal numbers and time formats.
        """
        text = "مقدار عدد پی تقریباً 3.14 و عدد اعشاری فارسی ۳.۱۴ است و زمان 14:45 می‌باشد."
        result = beautify_persian_spacing(text)
        self.assertIn("3.14", result)
        self.assertNotIn("3. 14", result)
        self.assertIn("14:45", result)
        self.assertNotIn("14: 45", result)

    def test_regression_standardize_persian_leading_and_trailing_zwnj(self):
        """
        Bug: standardize_persian previously stripped only ASCII spaces via .strip(),
             leaving leading and trailing ZWNJs untouched (\u200Cمتن\u200C).
        Fix: Strip leading and trailing ZWNJ characters from the output string.
        """
        text = "\u200Cمتن فارسی استاندارد\u200C"
        result = standardize_persian(text)
        self.assertFalse(result.startswith("\u200C"))
        self.assertFalse(result.endswith("\u200C"))
        self.assertEqual(result, "متن فارسی استاندارد")

    def test_regression_standardize_persian_space_adjacent_zwnj(self):
        """
        Bug: Inputs with spaces adjacent to ZWNJ (e.g. 'کتاب \\u200C ها' or 'کتاب\\u200C ها')
             resulted in invalid space-ZWNJ pairings ('کتاب \\u200cها').
        Fix: Clean up spaces adjacent to ZWNJ and collapse into clean half-spaces.
        """
        self.assertEqual(standardize_persian("کتاب \u200C ها"), "کتاب\u200Cها")
        self.assertEqual(standardize_persian("کتاب \u200Cها"), "کتاب\u200Cها")
        self.assertEqual(standardize_persian("کتاب\u200C ها"), "کتاب\u200Cها")

    def test_regression_reshaper_arabic_kaf_and_yeh(self):
        """
        Bug: In parsikit/reshaper.py, _SHAPES did not map Arabic Kaf ('\\u0643') or
             Arabic Yeh ('\\u064A'), leaving them unshaped and disconnected in graphical output.
        Fix: Map Arabic Kaf, Yeh, and Alef Maksura to appropriate presentation forms.
        """
        # Arabic Kaf
        arabic_kaf_result = reshape_for_graphics("كتاب")
        persian_kaf_result = reshape_for_graphics("کتاب")
        self.assertEqual(arabic_kaf_result, persian_kaf_result)

        # Arabic Yeh
        arabic_yeh_result = reshape_for_graphics("علي")
        persian_yeh_result = reshape_for_graphics("علی")
        self.assertEqual(arabic_yeh_result, persian_yeh_result)

    def test_regression_unicode_nfd_canonical_equivalence(self):
        """
        Bug: Decomposed NFD strings (such as decomposed 'آ' = Alef + Maddah) were not
             canonically normalized, failing equality tests against standard Persian strings.
        Fix: standardize_persian applies unicodedata.normalize('NFC', text).
        """
        nfd_str = unicodedata.normalize("NFD", "آسمان آبی")
        self.assertNotEqual(nfd_str, "آسمان آبی")  # Differ in byte/char composition
        nfc_result = standardize_persian(nfd_str)
        self.assertEqual(nfc_result, "آسمان آبی")

    def test_regression_reshaper_persian_digits_directionality(self):
        """
        Bug: Persian/Arabic digits were previously classified as RTL characters, causing
             numbers like 'سال ۱۴۰۳' to be inverted into 'ﻝﺎﺳ ۳۰۴۱'.
        Fix: Exclude digits from RTL reversing, ensuring numbers remain in proper LTR reading order.
        """
        shaped_persian_year = reshape_for_graphics("سال ۱۴۰۳")
        self.assertIn("۱۴۰۳", shaped_persian_year)
        self.assertNotIn("۳۰۴۱", shaped_persian_year)

        shaped_float = reshape_for_graphics("۱۲.۵")
        self.assertEqual(shaped_float, "۱۲.۵")

    def test_regression_reshaper_diacritic_combining_reversal(self):
        """
        Bug: When reversing RTL text blocks, combining diacritics were placed before their base glyphs,
             corrupting font rendering and causing detached diacritics.
        Fix: Cluster base characters with their trailing diacritics before reversing.
        """
        # 'بَ' -> Ba followed by Fatha. In shaped reversed stream, Fatha must still follow Ba.
        result = reshape_for_graphics("بَ")
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0], '\uFE8F')  # Isolated Ba
        self.assertEqual(result[1], '\u064E')  # Fatha

    def test_regression_reshaper_heh_with_yeh_above(self):
        """
        Bug: 'ۀ' (\u06C0) was missing from _SHAPES, leaving it unshaped and preventing preceding letters from connecting.
        Fix: Add 'ۀ' to _SHAPES with isolated (\uFBA4) and final (\uFBA5) presentation forms.
        """
        shaped = reshape_for_graphics("خانۀ", reverse=False)
        self.assertIn("\uFBA5", shaped)  # Final form of Heh with Yeh above

    def test_regression_reshaper_paragraph_newlines_and_validation(self):
        """
        Bug: reshape_paragraph_for_graphics split only by space, preserving embedded newlines inside list elements,
             and lacked validation for invalid max_chars_per_line.
        Fix: Split by paragraphs/newlines, wrap lines cleanly, and raise ValueError for max_chars_per_line <= 0.
        """
        lines = reshape_paragraph_for_graphics("خط اول\nخط دوم", max_chars_per_line=30)
        self.assertEqual(len(lines), 2)
        for line in lines:
            self.assertNotIn("\n", line)

        with self.assertRaises(ValueError):
            reshape_paragraph_for_graphics("سلام", max_chars_per_line=0)
        with self.assertRaises(ValueError):
            reshape_paragraph_for_graphics("سلام", max_chars_per_line=-5)

    def test_regression_persian_collation_alef_variants(self):
        """
        Bug: Arabic Alef variants like 'إ' (\u0625) and 'أ' (\u0623) were unmapped in _SORT_NORM_MAP,
             falling back to ord() > 1500 and sorting AFTER all Persian letters.
        Fix: Map 'أ', 'إ', 'ٱ', 'ؤ', 'ئ' to standard Persian letters in collation normalization.
        """
        from parsikit.text import persian_sorted
        words = ["امید", "احمد", "إحسان", "آذر"]
        sorted_words = persian_sorted(words)
        self.assertEqual(sorted_words, ["آذر", "إحسان", "احمد", "امید"])

    def test_regression_words_to_number_compound_scales(self):
        """
        Bug: Large composite scales like 'هزار میلیارد' (one trillion) or 'دویست هزار میلیارد'
             were parsed as additive groups (1000001000) instead of multiplicative magnitudes.
        Fix: Multiply previous accumulated scale group when an equal or larger scale is encountered.
        """
        from parsikit.text import words_to_number
        self.assertEqual(words_to_number("هزار میلیارد"), 1_000_000_000_000)
        self.assertEqual(words_to_number("دویست هزار میلیارد"), 200_000_000_000_000)

    def test_regression_beautify_spacing_open_paren_and_guillemets(self):
        """
        Bug: beautify_persian_spacing trimmed closing parens but not opening parens,
             and did not trim inner spaces in Persian guillemets « ... ».
        Fix: Cleanly trim inner margins for parentheses and Persian quotation guillemets.
        """
        text = "متن ( داخل پرانتز ) و « داخل گیومه » است."
        cleaned = beautify_persian_spacing(text)
        self.assertIn("(داخل پرانتز)", cleaned)
        self.assertIn("«داخل گیومه»", cleaned)

    def test_regression_extract_mobiles_and_national_codes_formatted(self):
        """
        Bug: extract_mobiles and extract_national_codes only matched purely contiguous digits,
             missing phone numbers or national codes written with hyphens or spaces.
        Fix: Support standard separator formats and clean them during validation.
        """
        from parsikit.text import extract_mobiles, extract_national_codes
        mob_text = "شماره‌های تماس: 0912-345-6789 و 0912 345 6789 و ۰۹۱۲۳۴۵۶۷۸۹."
        extracted_mobiles = extract_mobiles(mob_text)
        self.assertIn("09123456789", extracted_mobiles)

        nc_text = "کد ملی 773-012345-2 و 773 012345 2 معتبر هستند."
        extracted_ncs = extract_national_codes(nc_text)
        self.assertIn("7730123452", extracted_ncs)


class TestTextPhase02_1Regressions(unittest.TestCase):
    """
    Focused regression hardening tests for Phase 02.1.
    Covers URL query string preservation, clean_text technical token preservation,
    Arabic/Kurdish character separation, ZWNJ whitespace boundaries, and reshaper bidi integrity.
    """

    def test_regression_url_query_spacing_preserved(self):
        """
        Bug: beautify_persian_spacing inserted a space after '?' in URLs with query parameters:
             'Visit https://example.com/a?x=1&y=2.' became 'Visit https://example.com/a? x=1&y=2.'.
        Fix: Protect URLs with token placeholders during punctuation spacing passes.
        """
        raw = "Visit https://example.com/a?x=1&y=2."
        result = beautify_persian_spacing(raw)
        self.assertEqual(result, "Visit https://example.com/a?x=1&y=2.")
        self.assertNotIn("? x", result)

    def test_regression_url_varieties_preserved(self):
        """
        Verify all required URL forms (query strings, fragments, ports, percent-encoding)
        remain completely intact in both beautify_persian_spacing and clean_text.
        """
        urls = [
            "https://example.com/a?x=1&y=2",
            "https://example.com/search?q=persian+text&page=2",
            "https://example.com/path#section",
            "https://example.com:8443/api/v1?enabled=true",
            "https://example.com/file%20name.png",
        ]
        for url in urls:
            beautified = beautify_persian_spacing(url)
            self.assertEqual(beautified, url, f"beautify altered URL: {url}")

            cleaned = clean_text(url)
            self.assertEqual(cleaned, url, f"clean_text altered URL: {url}")
            # Ensure ASCII digits inside URLs were NOT converted to Persian digits
            self.assertFalse(any('\u06F0' <= c <= '\u06F9' for c in cleaned), f"Persian digits found in cleaned URL: {cleaned}")

    def test_regression_email_varieties_preserved(self):
        """
        Verify standard and tagged email addresses remain intact without punctuation spacing damage
        or digit corruption.
        """
        emails = [
            "user@example.com",
            "user.name+tag@example.co.uk",
        ]
        for email in emails:
            self.assertEqual(beautify_persian_spacing(email), email)
            self.assertEqual(clean_text(email), email)

    def test_regression_technical_tokens_digits_preserved_in_clean_text(self):
        """
        Bug: clean_text converted ASCII digits inside technical strings (versions, IDs) into Persian digits.
        Fix: Protect technical identifiers and version strings while converting prose numbers.
        """
        sample = "سیستم Python 3.13.3 با شناسه ID-2026-0042 و تنظیمات version=v2.0.1 فعال است و 25 روز مهلت دارد."
        cleaned = clean_text(sample)

        # Technical tokens preserved with ASCII digits
        self.assertIn("Python 3.13.3", cleaned)
        self.assertIn("ID-2026-0042", cleaned)
        self.assertIn("version=v2.0.1", cleaned)

        # Ordinary prose numbers converted to Persian digits
        self.assertIn("۲۵ روز", cleaned)
        self.assertNotIn("25 روز", cleaned)

    def test_regression_punctuation_around_urls_and_parens(self):
        """
        Verify trailing sentence punctuation after URLs is handled properly and
        closing parentheses followed by punctuation do not acquire unwanted spaces.
        """
        sentence = "لطفاً به آدرس (https://example.com/a?x=1&y=2) مراجعه کنید."
        beautified = beautify_persian_spacing(sentence)
        self.assertIn("(https://example.com/a?x=1&y=2)", beautified)
        self.assertNotIn("? x", beautified)

        # Period immediately following URL
        url_end = "آدرس وب‌سایت https://example.com/test."
        self.assertEqual(beautify_persian_spacing(url_end), "آدرس وب‌سایت https://example.com/test.")

        # Persian comma immediately following URL
        url_comma = "به آدرس https://example.com/a?x=1&y=2، مراجعه فرمایید."
        self.assertEqual(beautify_persian_spacing(url_comma), "به آدرس https://example.com/a?x=1&y=2، مراجعه فرمایید.")

        # Parenthesis followed by dot: no space before dot!
        paren_dot = "متن (داخل پرانتز)."
        self.assertEqual(beautify_persian_spacing(paren_dot), "متن (داخل پرانتز).")

        # Parenthesis followed by Persian comma: no space before comma!
        paren_comma = "متن (داخل پرانتز)، ادامه متن."
        self.assertEqual(beautify_persian_spacing(paren_comma), "متن (داخل پرانتز)، ادامه متن.")

    def test_regression_kurdish_text_preservation(self):
        """
        Bug: Kurdish Ae ('\u06D5' / 'ە') was previously mapped to Persian Heh ('\u0647'),
             corrupting Kurdish words like 'لە' into 'له'.
        Fix: Removed Kurdish Ae from Arabic-to-Persian table.
        """
        kurdish_text = "لە کوردی"
        normalized = standardize_persian(kurdish_text)
        self.assertEqual(normalized, "لە کوردی")
        self.assertIn("\u06D5", normalized)
        self.assertNotIn("له کوردی", normalized)

        more_kurdish = "ئەمە لە کوردیە"
        self.assertEqual(standardize_persian(more_kurdish), "ئەمە لە کوردیە")

    def test_regression_arabic_text_preservation_option(self):
        """
        Bug: Arabic Ta Marbuta ('ة') and Arabic Yeh ('ي') were unconditionally converted to 'ه' and 'ی',
             corrupting Arabic text like 'هذه لغة عربية جميلة' into 'هذه لغه عربیه جمیله'.
        Fix: Add preserve_arabic=True option to preserve Arabic-specific orthography.
        """
        arabic_text = "هذه لغة عربية جميلة"

        # With preserve_arabic=True: Arabic letters remain intact
        preserved = standardize_persian(arabic_text, preserve_arabic=True)
        self.assertEqual(preserved, "هذه لغة عربية جميلة")
        self.assertIn("ة", preserved)
        self.assertIn("ي", preserved)

        # clean_text also respects preserve_arabic
        cleaned_arabic = clean_text(arabic_text, preserve_arabic=True)
        self.assertEqual(cleaned_arabic, "هذه لغة عربية جميلة")

        # Default Persian context continues standard loanword normalization
        persian_loanwords = "كتابخانه ي ملي و مركز دايرة المعارف"
        normalized_persian = standardize_persian(persian_loanwords)
        self.assertEqual(normalized_persian, "کتابخانه ی ملی و مرکز دایره المعارف")

    def test_regression_zwnj_space_semantics_and_boundaries(self):
        """
        Bug: 'الف \\u200c ب' was aggressively collapsed into 'الف\\u200cب' (rendering as 'الفب').
        Fix: Collapse space+ZWNJ+space between independent words into a single regular space,
             while preserving prefixes, suffixes, and meaningful Persian half-spaces.
        """
        # Independent words with space on both sides of ZWNJ: keep separated with regular space
        self.assertEqual(standardize_persian("الف \u200c ب"), "الف ب")
        self.assertEqual(standardize_persian("سلام \u200c دنیا"), "سلام دنیا")

        # Prefixes and suffixes: properly attach with ZWNJ
        self.assertEqual(standardize_persian("کتاب \u200C ها"), "کتاب\u200Cها")
        self.assertEqual(standardize_persian("کتاب \u200Cها"), "کتاب\u200Cها")
        self.assertEqual(standardize_persian("کتاب\u200C ها"), "کتاب\u200Cها")
        self.assertEqual(standardize_persian("می \u200C روم"), "می\u200Cروم")
        self.assertEqual(standardize_persian("بی \u200C نهایت"), "بی\u200Cنهایت")

        # Meaningful half-spaces with single-sided space: preserve as ZWNJ
        self.assertEqual(standardize_persian("دانش \u200cآموز"), "دانش\u200cآموز")
        self.assertEqual(standardize_persian("دانش\u200c آموز"), "دانش\u200cآموز")

        # Line breaks preserved
        multiline = "خط اول: کتاب ها\nخط دوم: می رود"
        self.assertEqual(standardize_persian(multiline), "خط اول: کتاب‌ها\nخط دوم: می‌رود")

        # Idempotence property verified across all samples
        test_inputs = [
            "الف \u200c ب",
            "کتاب \u200C ها",
            "دانش \u200cآموز",
            "خط اول: کتاب ها\nخط دوم: می رود",
            "https://example.com/a?x=1&y=2",
            "Python 3.13.3",
        ]
        for inp in test_inputs:
            p1 = standardize_persian(inp)
            p2 = standardize_persian(p1)
            self.assertEqual(p1, p2, f"Idempotence failed for {inp!r}")

    def test_regression_reshaper_mixed_language_and_technical(self):
        """
        Verify reshaper behaves deterministically for Persian, English, mixed-language sentences,
        numbers, dates, URLs, Kurdish Ae, and combining diacritics.
        """
        # 1. Persian only
        shaped_fa = reshape_for_graphics("سلام")
        self.assertEqual(shaped_fa, "ﻡﻼﺳ")
        self.assertEqual(reshape_for_graphics("سلام", reverse=False), "ﺳﻼﻡ")

        # 2. English only (preserved intact)
        self.assertEqual(reshape_for_graphics("Hello World!"), "Hello World!")
        self.assertEqual(reshape_for_graphics("Hello World!", reverse=False), "Hello World!")

        # 3. Mixed Persian and English in same sentence
        mixed = "زبان Python بسیار محبوب است."
        shaped_mixed = reshape_for_graphics(mixed)
        self.assertIn("Python", shaped_mixed)

        # 4. Numbers, dates, version numbers
        date_ver = "تاریخ 2026/10/21 و نسخه 3.13.3 منتشر شد!"
        shaped_date = reshape_for_graphics(date_ver)
        self.assertIn("2026/10/21", shaped_date)
        self.assertIn("3.13.3", shaped_date)

        # 5. Embedded URLs and emails
        url_text = "آدرس https://example.com/a?x=1&y=2 و ایمیل user@example.com است"
        shaped_url = reshape_for_graphics(url_text)
        self.assertIn("https://example.com/a?x=1&y=2", shaped_url)
        self.assertIn("user@example.com", shaped_url)

        # 6. Kurdish Ae shaped connection
        kurdish_shaped = reshape_for_graphics("لە", reverse=False)
        self.assertEqual(kurdish_shaped, "\uFEDF\uFEEA")  # Initial Lam connected to final Heh

        # 7. ZWNJ and combining diacritics
        with_zwnj = reshape_for_graphics("می\u200cروم", reverse=False)
        self.assertIn("\u200C", with_zwnj)

        with_diacritic = reshape_for_graphics("بَ")
        self.assertEqual(with_diacritic[0], '\uFE8F')  # Isolated Ba
        self.assertEqual(with_diacritic[1], '\u064E')  # Fatha attached


if __name__ == "__main__":
    unittest.main()

