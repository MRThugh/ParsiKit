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


if __name__ == "__main__":
    unittest.main()
