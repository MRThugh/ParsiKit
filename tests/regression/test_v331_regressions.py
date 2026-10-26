"""
Regression tests for all verified defects fixed in ParsiKit v3.3.1.
Each test verifies a specific bug reproduction and resolution.
"""
import unittest
import datetime
import parsikit
from parsikit.datetime import is_jalali_leap, humanize_relative_time
from parsikit.validators import format_postal_code, is_valid_national_code
from parsikit.dev import pformat, persian_fstring, inspect_text
from parsikit.text import slugify, standardize_persian, mask_email


class TestV331Regressions(unittest.TestCase):
    def test_regression_jalali_leap_year_calculation(self):
        """
        Bug: is_jalali_leap(1399) returned False and 1400 returned True due to a 1-year shift.
        Fix: Correct astronomical 33-year cycle algorithm matching jalali_to_gregorian.
        """
        self.assertTrue(is_jalali_leap(1391))
        self.assertTrue(is_jalali_leap(1395))
        self.assertTrue(is_jalali_leap(1399))
        self.assertTrue(is_jalali_leap(1403))
        self.assertTrue(is_jalali_leap(1408))

        self.assertFalse(is_jalali_leap(1398))
        self.assertFalse(is_jalali_leap(1400))
        self.assertFalse(is_jalali_leap(1401))
        self.assertFalse(is_jalali_leap(1402))
        self.assertFalse(is_jalali_leap(1404))

    def test_regression_format_postal_code_layout(self):
        """
        Bug: format_postal_code previously returned XXX-XXXXXX-X (3-6-1 national code layout)
             due to a copy-paste error from format_national_code.
        Fix: Correctly format 10-digit postal codes as XXXXX-XXXXX (5-5 layout).
        """
        formatted = format_postal_code("1234567890")
        self.assertEqual(formatted, "12345-67890")
        self.assertEqual(len(formatted), 11)

    def test_regression_persian_comma_in_pformat_and_fstring(self):
        """
        Bug: pformat and persian_fstring with :,fa or :,p left ASCII comma ','
             instead of Persian comma '،'.
        Fix: Convert thousands separator comma to '،' when Persian digits are active.
        """
        res_pformat = pformat("{:>10,fa}", 15000)
        self.assertEqual(res_pformat, "    ۱۵،۰۰۰")

        price = 15000000
        res_fstring = persian_fstring("قیمت: {price:,fa} ریال")
        self.assertEqual(res_fstring, "قیمت: ۱۵،۰۰۰،۰۰۰ ریال")

    def test_regression_slugify_neskheh_pinglish(self):
        """
        Bug: slugify('سایت WordPress نسخه 6') fell back to 'site-wordpress-nskhh-6'
             because 'نسخه' was missing from _COMMON_WORDS_PINGLISH.
        Fix: Added 'نسخه': 'neskheh' to the Pinglish transliteration dictionary.
        """
        self.assertEqual(
            slugify("سایت WordPress نسخه 6"),
            "site-wordpress-neskheh-6"
        )

    def test_regression_humanize_relative_time_persian_numerals(self):
        """
        Bug: humanize_relative_time formatted numbers with ASCII digits (e.g. '5 دقیقه پیش')
             instead of Persian digits ('۵ دقیقه پیش').
        Fix: Pass numeric values through english_to_persian.
        """
        ref = datetime.datetime(2026, 7, 6, 12, 0, 0)
        dt = datetime.datetime(2026, 7, 6, 11, 55, 0)
        self.assertEqual(humanize_relative_time(dt, reference=ref), "۵ دقیقه پیش")

        dt_hours = datetime.datetime(2026, 7, 6, 9, 0, 0)
        self.assertEqual(humanize_relative_time(dt_hours, reference=ref), "۳ ساعت پیش")

        dt_days = datetime.datetime(2026, 7, 1, 12, 0, 0)
        self.assertEqual(humanize_relative_time(dt_days, reference=ref), "۵ روز پیش")

    def test_regression_standardize_duplicate_zwnj(self):
        """
        Bug: Accidental duplicate zero-width non-joiners (\\u200C\\u200C) corrupted
             string lengths and visual widths.
        Fix: Collapse consecutive ZWNJs in standardize_persian.
        """
        res = standardize_persian("کتاب\u200C\u200Cها")
        self.assertEqual(res, "کتاب\u200Cها")
        self.assertEqual(len(res), 7)

    def test_regression_national_code_checksum_verification(self):
        """
        Bug: Test fixture 0010123451 was mathematically invalid (remainder 3 requires check digit 8).
        Fix: Verified 0010123458 is valid with Tehran central location.
        """
        self.assertFalse(is_valid_national_code("0010123451"))
        self.assertTrue(is_valid_national_code("0010123458"))
        nc = parsikit.NationalCode("0010123458")
        self.assertEqual(nc.location["province"], "تهران")  # type: ignore

    def test_regression_inspect_text_numeral_metrics(self):
        """
        Bug: inspect_text did not return has_persian_digits metric.
        Fix: Added has_persian_digits to inspect_text returned dictionary.
        """
        analysis = inspect_text("متن فارسی با رقم ۱۲۳")
        self.assertTrue(analysis["has_persian_digits"])
        self.assertFalse(analysis["has_english_digits"])

    def test_regression_mask_email_middle_length(self):
        """
        Bug: mask_email accurately preserves 1-to-1 character masking for the 8 middle
             characters of kamrani.exe (produces 8 asterisks, not 6).
        """
        masked = mask_email("kamrani.exe@gmail.com")
        self.assertEqual(masked, "ka********e@gmail.com")

    def test_regression_terminal_color_detection_and_no_color(self):
        """
        Bug: _supports_color accessed sys.environ causing AttributeError on Windows,
             and ignored standard NO_COLOR / FORCE_COLOR variables.
        Fix: Use os.environ and properly honor NO_COLOR, FORCE_COLOR, and Windows Terminal.
        """
        from parsikit.dev import _supports_color
        import os
        orig_no = os.environ.get("NO_COLOR")
        orig_force = os.environ.get("FORCE_COLOR")
        try:
            os.environ["NO_COLOR"] = "1"
            if "FORCE_COLOR" in os.environ:
                del os.environ["FORCE_COLOR"]
            self.assertFalse(_supports_color())

            os.environ["FORCE_COLOR"] = "1"
            self.assertTrue(_supports_color())
        finally:
            if orig_no is not None:
                os.environ["NO_COLOR"] = orig_no
            elif "NO_COLOR" in os.environ:
                del os.environ["NO_COLOR"]
            if orig_force is not None:
                os.environ["FORCE_COLOR"] = orig_force
            elif "FORCE_COLOR" in os.environ:
                del os.environ["FORCE_COLOR"]

    def test_regression_pformat_zero_padding_and_visual_width(self):
        """
        Bug: pformat with zero-padding (e.g. {:05d}) stripped padding and filled with spaces.
             Also Unicode visual width ignored zero-width joiners, marks, and wide characters.
        Fix: Properly support zero-padding in PersianFormatter and accurate Unicode monospace width.
        """
        self.assertEqual(pformat("{:05d}", 42), "00042")
        self.assertEqual(pformat("{:05fa}", 42), "۰۰۰۴۲")

        # Test ZWJ and LRM have zero width
        zwnj_zwj_text = "تست\u200D\u200C"
        formatted = pformat("{:<8}", zwnj_zwj_text)
        self.assertEqual(formatted, "تست\u200D\u200C     ")

    def test_regression_national_code_short_length_rejection(self):
        """
        Bug: is_valid_national_code('27') returned True due to unrestricted zfill(10).
             National codes with fewer than 8 digits are mathematically and administratively invalid.
        Fix: Require length of clean digits to be between 8 and 10.
        """
        self.assertFalse(is_valid_national_code("27"))
        self.assertFalse(is_valid_national_code("123"))
        self.assertFalse(is_valid_national_code("0010123458abc"))

    def test_regression_validators_reject_invalid_letters(self):
        """
        Bug: is_valid_mobile, is_valid_card_number, is_valid_postal_code silently
             stripped letters, accepting inputs like '09123456789abc' or '6037991122334455xyz'.
        Fix: Reject strings containing letters or disallowed characters.
        """
        self.assertFalse(parsikit.is_valid_mobile("09123456789abc"))
        self.assertFalse(parsikit.is_valid_card_number("6037991122334455xyz"))
        self.assertFalse(parsikit.is_valid_postal_code("1234567890xyz"))
        self.assertFalse(parsikit.is_valid_corporate_id("11111111111xyz"))
        self.assertFalse(parsikit.is_valid_landline("02188888888xyz"))

    def test_regression_model_comparison_and_sorting(self):
        """
        Bug: Sorting domain models raised TypeError ('<' not supported).
        Fix: Added comparison operators to StringLikeMixin.
        """
        m1 = parsikit.MobileNumber("09123456788")
        m2 = parsikit.MobileNumber("09123456789")
        self.assertEqual(sorted([m2, m1]), [m1, m2])
        self.assertTrue(m1 < m2)
        self.assertTrue(m1 <= m2)
        self.assertTrue(m2 > m1)
        self.assertTrue(m2 >= m1)

    def test_regression_non_strict_models_safe_fallbacks(self):
        """
        Bug: Accessing .formatted, .masked, or .to_dict() on BankCard or Sheba with strict=False
             crashed with ValueError when input was invalid.
        Fix: Provide safe fallbacks without raising unhandled exceptions in strict=False mode.
        """
        card = parsikit.BankCard("123", strict=False)
        self.assertEqual(card.formatted, "123")
        self.assertIn("masked", card.to_dict())

        sheba = parsikit.Sheba("123", strict=False)
        self.assertEqual(sheba.formatted, "123")
        self.assertEqual(sheba.account_number, "")
        self.assertIn("bank", sheba.to_dict())

        nc = parsikit.NationalCode("123456789012", strict=False)
        self.assertEqual(nc.formatted, "123456789012")

    def test_regression_exception_privacy_masking(self):
        """
        Bug: InvalidMobileError and InvalidShebaError exposed plaintext numbers in exception messages.
        Fix: Mask sensitive middle digits in exception messages.
        """
        with self.assertRaises(parsikit.InvalidMobileError) as ctx_mob:
            parsikit.MobileNumber("0912345678")
        self.assertNotIn("0912345678", str(ctx_mob.exception))
        self.assertIn("0912***678", str(ctx_mob.exception))

        with self.assertRaises(parsikit.InvalidShebaError) as ctx_sheba:
            parsikit.Sheba("IR000123456789012345678901")
        self.assertNotIn("0123456789012345678901", str(ctx_sheba.exception))
        self.assertIn("IR00****", str(ctx_sheba.exception))

    def test_regression_add_tax_and_toll_breakdown(self):
        """
        Feature: add_tax_and_toll supports optional breakdown=True returning a detailed dict.
        """
        res = parsikit.add_tax_and_toll(100000, breakdown=True)
        self.assertIsInstance(res, dict)
        self.assertEqual(res["total"], 110000)
        self.assertEqual(res["tax"], 10000)
        self.assertEqual(res["base"], 100000)

    def test_regression_datetime_boundary_validation(self):
        """
        Bug: Invalid month or day in gregorian_to_jalali and jalali_to_gregorian raised IndexError.
        Fix: Explicitly validate bounds and raise ValueError.
        """
        with self.assertRaises(ValueError):
            parsikit.gregorian_to_jalali(2026, 13, 1)
        with self.assertRaises(ValueError):
            parsikit.jalali_to_gregorian(1405, 13, 1)

    def test_regression_format_jalali_persian_digits(self):
        """
        Feature: format_jalali supports persian_digits=True.
        """
        fmt = parsikit.format_jalali(1405, 7, 15, persian_digits=True)
        self.assertEqual(fmt, "۱۴۰۵/۰۷/۱۵")

    def test_feature_bidirectional_keyboard_correction(self):
        """
        Feature 4: Bidirectional keyboard layout correction ('persian', 'english', 'auto').
        """
        self.assertEqual(parsikit.correct_keyboard_layout("sghl", to="persian"), "سلام")
        self.assertEqual(parsikit.correct_keyboard_layout("اثممخ", to="english"), "hello")
        self.assertEqual(parsikit.correct_keyboard_layout("sghl", to="auto"), "سلام")
        # Preserves already-correct Persian text
        self.assertEqual(parsikit.correct_keyboard_layout("سلام دوستان", to="persian"), "سلام دوستان")

    def test_feature_normalize_digits(self):
        """
        Feature 2: Digits normalization to Persian, English, or Arabic.
        """
        self.assertEqual(parsikit.normalize_digits("کد 123 و ٤٥٦", to="persian"), "کد ۱۲۳ و ۴۵۶")
        self.assertEqual(parsikit.normalize_digits("کد ۱۲۳", to="english"), "کد 123")
        self.assertEqual(parsikit.normalize_digits("کد 123", to="arabic"), "کد ١٢٣")

    def test_feature_smart_persian_spacing(self):
        """
        Feature 3: Optional smart Persian spacing and punctuation correction.
        """
        text = "کتاب  ها  می رود  و  سریع تر  است ."
        res = parsikit.smart_persian_spacing(text)
        self.assertIn("کتاب‌ها", res)
        self.assertIn("می‌رود", res)
        self.assertIn("سریع‌تر", res)
        self.assertTrue(res.endswith("است."))

    def test_feature_expand_snippets(self):
        """
        Feature 5: Configurable snippet expansion with boundary protection.
        """
        snippets = {"//salam": "سلام و درود", "//em": "test@example.com"}
        text = "پیام: //salam به شما!"
        res = parsikit.expand_snippets(text, snippets)
        self.assertEqual(res, "پیام: سلام و درود به شما!")


if __name__ == "__main__":
    unittest.main()

