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


if __name__ == "__main__":
    unittest.main()
