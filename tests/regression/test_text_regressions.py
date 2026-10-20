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


if __name__ == "__main__":
    unittest.main()
