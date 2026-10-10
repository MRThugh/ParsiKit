"""Unit tests for parsikit.datetime module."""
import unittest
import datetime
from parsikit.datetime import (
    gregorian_to_jalali, jalali_to_gregorian, format_jalali,
    get_jalali_month_name, is_jalali_leap, humanize_relative_time
)


class TestDatetimeModule(unittest.TestCase):
    def test_gregorian_to_jalali(self):
        # Nowruz 1403
        self.assertEqual(gregorian_to_jalali(2024, 3, 20), (1403, 1, 1))
        # Known milestone date
        self.assertEqual(gregorian_to_jalali(2026, 7, 6), (1405, 4, 15))

    def test_jalali_to_gregorian(self):
        self.assertEqual(jalali_to_gregorian(1403, 1, 1), (2024, 3, 20))
        self.assertEqual(jalali_to_gregorian(1405, 4, 15), (2026, 7, 6))

    def test_round_trip_conversion(self):
        for gy in [2020, 2021, 2022, 2023, 2024, 2025, 2026]:
            for gm in [1, 6, 12]:
                for gd in [1, 15, 28]:
                    jy, jm, jd = gregorian_to_jalali(gy, gm, gd)
                    gy_back, gm_back, gd_back = jalali_to_gregorian(jy, jm, jd)
                    self.assertEqual((gy, gm, gd), (gy_back, gm_back, gd_back))

    def test_format_jalali(self):
        self.assertEqual(format_jalali(1403, 1, 5), "1403/01/05")
        self.assertEqual(format_jalali(1403, 1, 5, pattern="YYYY-MM-DD"), "1403-01-05")
        self.assertEqual(format_jalali(1403, 12, 29, pattern="DD/MM/YYYY"), "29/12/1403")

    def test_get_jalali_month_name(self):
        self.assertEqual(get_jalali_month_name(1), "فروردین")
        self.assertEqual(get_jalali_month_name(7), "مهر")
        self.assertEqual(get_jalali_month_name(12), "اسفند")

        with self.assertRaises(ValueError):
            get_jalali_month_name(0)
        with self.assertRaises(ValueError):
            get_jalali_month_name(13)

    def test_is_jalali_leap(self):
        # Known Iranian calendar leap years
        self.assertTrue(is_jalali_leap(1391))
        self.assertTrue(is_jalali_leap(1395))
        self.assertTrue(is_jalali_leap(1399))
        self.assertTrue(is_jalali_leap(1403))
        self.assertTrue(is_jalali_leap(1408))

        # Known non-leap years
        self.assertFalse(is_jalali_leap(1398))
        self.assertFalse(is_jalali_leap(1400))
        self.assertFalse(is_jalali_leap(1401))
        self.assertFalse(is_jalali_leap(1402))
        self.assertFalse(is_jalali_leap(1404))

    def test_humanize_relative_time(self):
        ref = datetime.datetime(2026, 7, 6, 12, 0, 0)

        # Seconds past
        dt = datetime.datetime(2026, 7, 6, 11, 59, 55)
        self.assertEqual(humanize_relative_time(dt, reference=ref), "هم‌اکنون")

        # Minutes past
        dt = datetime.datetime(2026, 7, 6, 11, 55, 0)
        self.assertEqual(humanize_relative_time(dt, reference=ref), "۵ دقیقه پیش")

        # Hours past
        dt = datetime.datetime(2026, 7, 6, 9, 0, 0)
        self.assertEqual(humanize_relative_time(dt, reference=ref), "۳ ساعت پیش")

        # 1 Hour past
        dt = datetime.datetime(2026, 7, 6, 11, 0, 0)
        self.assertEqual(humanize_relative_time(dt, reference=ref), "۱ ساعت پیش")

        # Yesterday
        dt = datetime.datetime(2026, 7, 5, 12, 0, 0)
        self.assertEqual(humanize_relative_time(dt, reference=ref), "دیروز")

        # Days past
        dt = datetime.datetime(2026, 7, 1, 12, 0, 0)
        self.assertEqual(humanize_relative_time(dt, reference=ref), "۵ روز پیش")

        # Months past
        dt = datetime.datetime(2026, 4, 1, 12, 0, 0)
        self.assertIn("ماه پیش", humanize_relative_time(dt, reference=ref))

        # Years past
        dt = datetime.datetime(2024, 7, 6, 12, 0, 0)
        self.assertIn("سال قبل", humanize_relative_time(dt, reference=ref))


if __name__ == "__main__":
    unittest.main()
