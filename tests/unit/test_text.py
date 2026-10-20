"""Unit tests for parsikit.text module."""
import unittest
import parsikit
from parsikit.text import (
    standardize_persian, strip_diacritics, is_persian, correct_keyboard_layout,
    persian_sort_key, persian_sorted, beautify_persian_spacing, extract_mobiles,
    extract_national_codes, words_to_number, slugify, clean_text,
    normalize_whitespace, convert_numbers, mask_mobile, mask_card,
    mask_national_code, mask_email
)


class TestTextProcessing(unittest.TestCase):
    def test_standardize_persian_basic(self):
        self.assertEqual(standardize_persian("ي كافيه ك"), "ی کافیه ک")
        self.assertEqual(standardize_persian("کتاب ها"), "کتاب‌ها")
        self.assertEqual(standardize_persian("می رود"), "می‌رود")
        self.assertEqual(standardize_persian("بی نهایت"), "بی‌نهایت")
        self.assertEqual(standardize_persian("سریع تر"), "سریع‌تر")
        self.assertEqual(standardize_persian("زیباترین ها"), "زیباترین‌ها")

    def test_standardize_persian_diacritics_option(self):
        text = "سَلام دُنیا"
        self.assertEqual(standardize_persian(text, strip_diacritics_opt=True), "سلام دنیا")
        self.assertEqual(standardize_persian(text, strip_diacritics_opt=False), "سَلام دُنیا")

    def test_standardize_duplicate_zwnj(self):
        self.assertEqual(standardize_persian("کتاب\u200C\u200Cها"), "کتاب\u200Cها")
        self.assertEqual(standardize_persian("می\u200C\u200C\u200Cرود"), "می\u200Cرود")

    def test_strip_diacritics(self):
        self.assertEqual(strip_diacritics("سَلامٌ عَلَیکُمْ"), "سلام علیکم")
        self.assertEqual(strip_diacritics(""), "")

    def test_is_persian(self):
        self.assertTrue(is_persian("سلام"))
        self.assertTrue(is_persian("English متن فارسی"))
        self.assertFalse(is_persian("Hello World! 12345"))
        self.assertFalse(is_persian(""))

    def test_correct_keyboard_layout(self):
        self.assertEqual(correct_keyboard_layout("sghl"), "سلام")
        self.assertEqual(correct_keyboard_layout("jvh"), "ترا")
        self.assertEqual(correct_keyboard_layout(""), "")

    def test_persian_sort_key_and_persian_sorted(self):
        words = ["سیب", "انار", "به", "هلو", "پرتقال", "آلو"]
        sorted_words = persian_sorted(words)
        self.assertEqual(sorted_words, ["آلو", "انار", "به", "پرتقال", "سیب", "هلو"])

    def test_beautify_persian_spacing(self):
        self.assertEqual(beautify_persian_spacing("سلام ,دنیا ;خوبی ?"), "سلام، دنیا؛ خوبی?")
        self.assertEqual(beautify_persian_spacing("متن (داخل پرانتز ) است"), "متن (داخل پرانتز) است")

    def test_extract_mobiles(self):
        text = "شماره من 09123456789 و همکارم +989351234567 است. شماره فیک 0912abc حساب نمیشه."
        mobiles = extract_mobiles(text)
        self.assertIn("09123456789", mobiles)
        self.assertIn("09351234567", mobiles)
        self.assertEqual(len(mobiles), 2)

    def test_extract_national_codes(self):
        text = "کد ملی اول 7730123452 و دومی 773-012345-2 و نامعتبر 1111111111 است."
        codes = extract_national_codes(text)
        self.assertEqual(codes, ["7730123452"])

    def test_words_to_number(self):
        self.assertEqual(words_to_number("صفر"), 0)
        self.assertEqual(words_to_number("دوازده"), 12)
        self.assertEqual(words_to_number("منفی پنجاه"), -50)
        self.assertEqual(words_to_number("سی و دو هزار و پانصد"), 32500)
        self.assertEqual(words_to_number("یک میلیون و دویست و پنجاه هزار"), 1250000)
        self.assertEqual(words_to_number("سه میلیارد و پانصد میلیون"), 3500000000)
        self.assertEqual(words_to_number("صد و پنجاه"), 150)
        self.assertEqual(words_to_number("یکصد و پنجاه"), 150)
        self.assertEqual(words_to_number(""), 0)

    def test_slugify(self):
        self.assertEqual(slugify("سلام دنیا"), "salam-donya")
        self.assertEqual(slugify("آموزش وردپرس"), "amoozesh-wordpress")
        self.assertEqual(slugify("سایت WordPress نسخه 6"), "site-wordpress-neskheh-6")
        self.assertEqual(slugify(""), "")

    def test_clean_text(self):
        dirty = "ي كافيه ك   کتاب  ها  ميباشد  ۱۱۲۳\n\n\n\nجدید  "
        cleaned = clean_text(dirty)
        self.assertIn("کتاب‌ها", cleaned)
        self.assertIn("میباشد", cleaned)
        self.assertIn("۱۱۲۳", cleaned)
        self.assertIn("\n\nجدید", cleaned)
        self.assertEqual(clean_text(""), "")

    def test_normalize_whitespace(self):
        self.assertEqual(normalize_whitespace("  سلام   دنیا  "), "سلام دنیا")
        paragraphs = "خط اول\n\n\n\nخط دوم   با   فاصله\n\nخط سوم"
        self.assertEqual(
            normalize_whitespace(paragraphs, keep_paragraphs=True),
            "خط اول\n\nخط دوم با فاصله\n\nخط سوم"
        )
        self.assertEqual(
            normalize_whitespace(paragraphs, keep_paragraphs=False),
            "خط اول خط دوم با فاصله خط سوم"
        )
        self.assertEqual(normalize_whitespace(""), "")

    def test_convert_numbers(self):
        self.assertEqual(convert_numbers("Price 12500", "persian"), "Price ۱۲۵۰۰")
        self.assertEqual(convert_numbers("قیمت ۱۲۵۰۰", "english"), "قیمت 12500")
        self.assertEqual(convert_numbers("123"), "۱۲۳")
        with self.assertRaises(ValueError):
            convert_numbers("123", "spanish")
        self.assertEqual(convert_numbers(""), "")

    def test_mask_mobile(self):
        self.assertEqual(mask_mobile("09123456789"), "0912***6789")
        self.assertEqual(mask_mobile("+989123456789"), "0912***6789")
        self.assertEqual(mask_mobile("09123456789", mask_char="X"), "0912XXX6789")
        self.assertEqual(mask_mobile(""), "")

    def test_mask_card(self):
        self.assertEqual(mask_card("6037-9911-2233-4455"), "6037-99**-****-4455")
        self.assertEqual(mask_card("6037991122334455"), "6037-99**-****-4455")
        self.assertEqual(mask_card("6037991122334455", mask_char="X"), "6037-99XX-XXXX-4455")
        self.assertEqual(mask_card(""), "")

    def test_mask_national_code(self):
        self.assertEqual(mask_national_code("7730123452"), "773-****45-2")
        self.assertEqual(mask_national_code("773-012345-2"), "773-****45-2")
        self.assertEqual(mask_national_code("7730123452", mask_char="X"), "773-XXXX45-2")
        self.assertEqual(mask_national_code(""), "")

    def test_mask_email(self):
        self.assertEqual(mask_email("ali@example.com"), "al***i@example.com")
        self.assertEqual(mask_email("kamrani.exe@gmail.com"), "ka********e@gmail.com")
        self.assertEqual(mask_email("ax@example.com"), "a*@example.com")
        self.assertEqual(mask_email("a@example.com"), "a*@example.com")
        self.assertEqual(mask_email(""), "")
        self.assertEqual(mask_email("not-an-email"), "not-an-email")

    def test_unicode_nfc_canonical_equivalence(self):
        """Verify that decomposed NFD Unicode sequences are canonically normalized to precomposed NFC."""
        import unicodedata
        # 'آ' precomposed is \u0622; decomposed is \u0627\u0653 (Alef + Maddah)
        decomposed = unicodedata.normalize("NFD", "آب و هوا")
        self.assertNotEqual(decomposed, "آب و هوا")  # Character sequences differ in NFD
        normalized = standardize_persian(decomposed)
        self.assertEqual(normalized, "آب و هوا")
        self.assertEqual(unicodedata.normalize("NFC", normalized), normalized)

    def test_arabic_letter_variants_normalization(self):
        """Verify standard Arabic Yeh, Kaf, and Ta Marbuta mapping in Persian context."""
        arabic_text = "كتابخانه ي ملي و مركز دايرة المعارف"
        normalized = standardize_persian(arabic_text)
        self.assertNotIn("ك", normalized)
        self.assertNotIn("ي", normalized)
        self.assertIn("ک", normalized)
        self.assertIn("ی", normalized)
        self.assertEqual(normalized, "کتابخانه ی ملی و مرکز دایره المعارف")

    def test_zwnj_leading_trailing_and_space_adjacent(self):
        """Verify leading, trailing, and space-adjacent ZWNJ are cleanly repaired."""
        # Leading and trailing ZWNJ
        self.assertEqual(standardize_persian("\u200Cکتاب\u200Cها\u200C"), "کتاب\u200Cها")
        self.assertEqual(standardize_persian("  \u200Cسلام\u200C  "), "سلام")

        # Space adjacent to ZWNJ: ' \u200C' or '\u200C '
        self.assertEqual(standardize_persian("کتاب \u200C ها"), "کتاب\u200Cها")
        self.assertEqual(standardize_persian("کتاب \u200Cها"), "کتاب\u200Cها")
        self.assertEqual(standardize_persian("کتاب\u200C ها"), "کتاب\u200Cها")

    def test_zwnj_adjacent_to_punctuation(self):
        """Verify ZWNJ adjacent to punctuation marks is removed as redundant."""
        self.assertEqual(standardize_persian("کتاب.\u200Cها"), "کتاب.ها")
        self.assertEqual(standardize_persian("جمله\u200C، کلمه"), "جمله، کلمه")
        self.assertEqual(standardize_persian("( \u200Cمتن\u200C )"), "(متن)")

    def test_standardize_persian_idempotence(self):
        """Verify the mathematical idempotence property: f(f(x)) == f(x)."""
        samples = [
            "کتاب ها و می رود و سریع تر و زیباترین ها",
            "  \u200Cکتاب\u200C\u200Cها\u200C  ",
            "ي كافيه ك   کتاب  ها  ميباشد  ۱۱۲۳",
            "سلام، دنیا! خوبی؟",
            "متن (تست داخل پرانتز) است.",
            "Python 3.10 و نسخه 6.0",
            "https://example.com/api?q=test",
            "شماره تماس 09123456789 است.",
            "",
            "   ",
        ]
        for s in samples:
            first_pass = standardize_persian(s)
            second_pass = standardize_persian(first_pass)
            self.assertEqual(
                first_pass, second_pass,
                f"Idempotence violation for input: {repr(s)}"
            )

    def test_beautify_persian_spacing_urls_and_emails_preserved(self):
        """Verify URLs, email addresses, and filenames are not broken by punctuation spacing."""
        text = "به وب‌سایت https://example.com/test بروید یا به kamrani.exe@gmail.com ایمیل بزنید."
        beautified = beautify_persian_spacing(text)
        self.assertIn("https://example.com/test", beautified)
        self.assertIn("kamrani.exe@gmail.com", beautified)

        code_text = "فایل script.min.js یا test.py را اجرا کنید."
        beautified_code = beautify_persian_spacing(code_text)
        self.assertIn("script.min.js", beautified_code)
        self.assertIn("test.py", beautified_code)

    def test_beautify_persian_spacing_decimals_and_time_preserved(self):
        """Verify decimal numbers and clock timestamps are preserved intact."""
        text = "عدد 3.14 و مقدار ۱۲.۵ در ساعت 12:30 ثبت شد."
        beautified = beautify_persian_spacing(text)
        self.assertIn("3.14", beautified)
        self.assertIn("۱۲.۵", beautified)
        self.assertIn("12:30", beautified)

    def test_beautify_persian_spacing_persian_punctuation(self):
        """Verify Persian punctuation spacing around commas, semicolons, colons, and question marks."""
        text = "سلام،خوبی؟نکته:مهم است؛ادامه دارد."
        beautified = beautify_persian_spacing(text)
        self.assertEqual(beautified, "سلام، خوبی؟ نکته: مهم است؛ ادامه دارد.")

    def test_slugify_prepositions_and_punctuation(self):
        """Verify slugify handles prepositions, clean separators, and mixed scripts."""
        self.assertEqual(slugify("کتاب در ایران"), "ketab-dar-iran")
        self.assertEqual(slugify("برنامه نویسی با پایتون"), "barnameh-nevisi-ba-python")
        self.assertEqual(slugify("راهنمای خرید از فروشگاه"), "rahnamaye-kharid-az-forooshgah")
        self.assertEqual(slugify("---سلام---دنیا---"), "salam-donya")
        self.assertEqual(slugify("تست", separator="_"), "tst")
        self.assertEqual(slugify(""), "")
        self.assertEqual(slugify("???!!!"), "")

    def test_persian_sort_key_return_type_and_ordering(self):
        """Verify persian_sort_key returns tuple and properly orders Persian alphabet."""
        key = persian_sort_key("سیب")
        self.assertIsInstance(key, tuple)
        self.assertGreater(len(key), 0)

        # Invalid type returns (0,)
        self.assertEqual(persian_sort_key(None), (0,))  # type: ignore

        # Alphabetical ordering
        items = ["گاو", "چتر", "پلنگ", "ژاله", "آب"]
        sorted_items = persian_sorted(items)
        self.assertEqual(sorted_items, ["آب", "پلنگ", "چتر", "ژاله", "گاو"])

    def test_empty_and_whitespace_only_inputs(self):
        """Verify consistent handling of empty and whitespace-only inputs across text utilities."""
        self.assertEqual(standardize_persian("   "), "")
        self.assertEqual(clean_text("   "), "")
        self.assertEqual(normalize_whitespace("   "), "")
        self.assertEqual(beautify_persian_spacing(""), "")
        self.assertEqual(strip_diacritics(""), "")
        self.assertFalse(is_persian("   "))
        self.assertEqual(words_to_number(""), 0)
        self.assertEqual(extract_mobiles(""), [])
        self.assertEqual(extract_national_codes(""), [])
        self.assertEqual(convert_numbers(""), "")


if __name__ == "__main__":
    unittest.main()
