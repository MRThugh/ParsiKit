"""Unit tests for parsikit.currency module."""
import unittest
import parsikit
from parsikit.currency import (
    format_currency, rial_to_toman, toman_to_rial, format_currency_to_words,
    add_tax_and_toll, calculate_installments
)


class TestCurrencyModule(unittest.TestCase):
    def setUp(self):
        parsikit.config.reset_defaults()

    def test_format_currency_default(self):
        # Default is Toman from config
        self.assertEqual(format_currency(15000), "15,000 تومان")
        self.assertEqual(format_currency("15000"), "15,000 تومان")
        self.assertEqual(format_currency("۱۵۰۰۰"), "15,000 تومان")

    def test_format_currency_persian_digits(self):
        self.assertEqual(
            format_currency(15000, "toman", persian_digits=True),
            "۱۵،۰۰۰ تومان"
        )
        self.assertEqual(
            format_currency(250000, "rial", persian_digits=True),
            "۲۵۰،۰۰۰ ریال"
        )

    def test_format_currency_invalid(self):
        with self.assertRaises(ValueError):
            format_currency(15000, "dollar")  # type: ignore
        with self.assertRaises(ValueError):
            format_currency("not_a_number")

    def test_rial_and_toman_conversion(self):
        self.assertEqual(rial_to_toman(10000), 1000)
        self.assertEqual(toman_to_rial(1000), 10000)
        self.assertEqual(rial_to_toman(0), 0)
        self.assertEqual(toman_to_rial(0), 0)

        with self.assertRaises(ValueError):
            rial_to_toman(-50)
        with self.assertRaises(ValueError):
            toman_to_rial(-50)

    def test_format_currency_to_words(self):
        self.assertEqual(format_currency_to_words(15000, "toman"), "پانزده هزار تومان")
        self.assertEqual(format_currency_to_words(500000, "rial"), "پانصد هزار ریال")
        self.assertEqual(format_currency_to_words("۱۵۰۰۰"), "پانزده هزار تومان")

        with self.assertRaises(ValueError):
            format_currency_to_words(100, "euro")  # type: ignore
        with self.assertRaises(ValueError):
            format_currency_to_words("invalid")

    def test_add_tax_and_toll(self):
        # Default rate is 10%
        self.assertEqual(add_tax_and_toll(100000), 110000)
        self.assertEqual(add_tax_and_toll("100000"), 110000)
        self.assertEqual(add_tax_and_toll("۱۰۰۰۰۰"), 110000)
        # Custom tax rate
        self.assertEqual(add_tax_and_toll(100000, tax_rate=0.09), 109000)

        with self.assertRaises(ValueError):
            add_tax_and_toll(-100)
        with self.assertRaises(ValueError):
            add_tax_and_toll("abc")

    def test_calculate_installments(self):
        # 12,000,000 loan with 0% interest over 12 months = 1,000,000 / month
        self.assertEqual(calculate_installments(12000000, 0, 12), 1000000)
        # Standard bank loan
        res = calculate_installments(100000000, 18.0, 12)
        self.assertGreater(res, 0)

        with self.assertRaises(ValueError):
            calculate_installments(-10, 10, 12)
        with self.assertRaises(ValueError):
            calculate_installments(100, 10, 0)
        with self.assertRaises(ValueError):
            calculate_installments("abc", 10, 12)


if __name__ == "__main__":
    unittest.main()
