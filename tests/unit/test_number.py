"""Unit tests for parsikit.number module."""
import unittest
from parsikit.number import english_to_persian, persian_to_english, number_to_words


class TestNumberModule(unittest.TestCase):
    def test_english_to_persian(self):
        self.assertEqual(english_to_persian("0123456789"), "۰۱۲۳۴۵۶۷۸۹")
        self.assertEqual(english_to_persian("Price: 1500 USD"), "Price: ۱۵۰۰ USD")
        # Arabic-indic digits conversion
        self.assertEqual(english_to_persian("٠١٢٣٤٥٦٧٨٩"), "۰۱۲۳۴۵۶۷۸۹")
        self.assertEqual(english_to_persian(""), "")

    def test_persian_to_english(self):
        self.assertEqual(persian_to_english("۰۱۲۳۴۵۶۷۸۹"), "0123456789")
        self.assertEqual(persian_to_english("قیمت: ۱۵۰۰ دلار"), "قیمت: 1500 دلار")
        self.assertEqual(persian_to_english("٠١٢٣٤٥٦٧٨٩"), "0123456789")
        self.assertEqual(persian_to_english(""), "")

    def test_number_to_words_basic(self):
        self.assertEqual(number_to_words(0), "صفر")
        self.assertEqual(number_to_words(5), "پنج")
        self.assertEqual(number_to_words(14), "چهارده")
        self.assertEqual(number_to_words(25), "بیست و پنج")
        self.assertEqual(number_to_words(100), "یکصد")
        self.assertEqual(number_to_words(325), "سیصد و بیست و پنج")
        self.assertEqual(number_to_words(1000), "هزار")
        self.assertEqual(number_to_words(12500), "دوازده هزار و پانصد")
        self.assertEqual(number_to_words(1000000), "یک میلیون")

    def test_number_to_words_negatives(self):
        self.assertEqual(number_to_words(-12), "منفی دوازده")
        self.assertEqual(number_to_words("-1250"), "منفی هزار و دویست و پنجاه")

    def test_number_to_words_string_inputs(self):
        self.assertEqual(number_to_words("15000"), "پانزده هزار")
        self.assertEqual(number_to_words("۱۵،۰۰۰"), "پانزده هزار")
        self.assertEqual(number_to_words("15,000"), "پانزده هزار")

    def test_number_to_words_invalid(self):
        with self.assertRaises(ValueError):
            number_to_words("abc")

    def test_number_to_words_large(self):
        self.assertEqual(number_to_words(1_000_000_000), "یک میلیارد")
        self.assertEqual(number_to_words(1_000_000_000_000), "یک تریلیون")


if __name__ == "__main__":
    unittest.main()
