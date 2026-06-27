"""
Comprehensive test suite for ParsiKit version 2.1.0.
"""

import unittest

from parsikit.text import standardize_persian, strip_diacritics, is_persian, correct_keyboard_layout
from parsikit.number import english_to_persian, persian_to_english, number_to_words
from parsikit.currency import (
    format_currency,
    rial_to_toman,
    toman_to_rial,
    format_currency_to_words,
    add_tax_and_toll,
    calculate_installments,
)
from parsikit.validators import (
    is_valid_national_code,
    format_national_code,
    is_valid_mobile,
    normalize_mobile,
    is_valid_card_number,
    format_card_number,
    is_valid_sheba,
    format_sheba,
)
from parsikit.reshaper import reshape_for_graphics


class TestText(unittest.TestCase):
    def test_standardize(self):
        self.assertEqual(standardize_persian("ي كافيه ك"), "ی کافیه ک")
        self.assertEqual(standardize_persian("می نویسم"), "می\u200Cنویسم")
        self.assertEqual(standardize_persian("سریع تر"), "سریع\u200Cتر")

    def test_bugs_not_triggered(self):
        self.assertEqual(standardize_persian("من هم رفتم"), "من هم رفتم")
        self.assertEqual(standardize_persian("هر روز"), "هر روز")

    def test_strip_diacritics(self):
        self.assertEqual(strip_diacritics("عَلِیّ"), "علی")

    def test_is_persian(self):
        self.assertTrue(is_persian("زبان فارسی"))
        self.assertFalse(is_persian("English Language"))

    def test_correct_keyboard_layout(self):
        self.assertEqual(correct_keyboard_layout("sghl"), "سلام")


class TestNumber(unittest.TestCase):
    def test_conversions(self):
        self.assertEqual(english_to_persian("987"), "۹۸۷")
        self.assertEqual(persian_to_english("۹۸۷"), "987")

    def test_to_words(self):
        self.assertEqual(number_to_words(0), "صفر")
        self.assertEqual(number_to_words("۱۲۵۰۰"), "دوازده هزار و پانصد")
        self.assertEqual(number_to_words(-12), "منفی دوازده")


class TestCurrency(unittest.TestCase):
    def test_formatting(self):
        self.assertEqual(format_currency(5000000), "5,000,000 تومان")
        self.assertEqual(format_currency(500000, persian_digits=True), "۵۰۰،۰۰۰ تومان")

    def test_conversions(self):
        self.assertEqual(rial_to_toman(10), 1)
        self.assertEqual(toman_to_rial(1), 10)

    def test_words(self):
        self.assertEqual(format_currency_to_words(1000000, "toman"), "یک میلیون تومان")

    def test_tax(self):
        self.assertEqual(add_tax_and_toll(100000), 110000)

    def test_installments(self):
        self.assertEqual(calculate_installments(10000000, 18.0, 12), 916799)


class TestValidators(unittest.TestCase):
    def test_national_code(self):
        self.assertTrue(is_valid_national_code("7730123452"))
        self.assertFalse(is_valid_national_code("1111111111"))
        self.assertEqual(format_national_code("7730123452"), "773-012345-2")

    def test_mobile(self):
        self.assertTrue(is_valid_mobile("+98۹۱۲۳۴۵۶۷۸۹"))
        self.assertEqual(normalize_mobile("09123456789", prefix="+98"), "+989123456789")

    def test_bank_card(self):
        self.assertTrue(is_valid_card_number("6037991122334455"))
        self.assertEqual(format_card_number("6037991122334455"), "6037-9911-2233-4455")

    def test_sheba(self):
        self.assertTrue(is_valid_sheba("IR050170000000123456789012"))
        self.assertEqual(
            format_sheba("050170000000123456789012"),
            "IR05 0170 0000 0012 3456 7890 12"
        )


class TestReshaper(unittest.TestCase):
    def test_basic_reshaping(self):
        # سلام -> 'س' (initial) + 'ل' (medial) + 'ا' (final) + 'م' (isolated)
        # FE8D + FEE0 + FE8E + FEE1
        # If reversed: isolated 'م' + final 'ا' + medial 'ل' + initial 'س'
        shaped_reversed = reshape_for_graphics("سلام")
        self.assertEqual(shaped_reversed, "ﻡﻼﺳ") # Standard reversed representation of سلام

    def test_mixed_reshaping(self):
        # English words should not be reversed or broken
        result = reshape_for_graphics("سلام Hello جهان")
        self.assertIn("Hello", result)
        self.assertTrue(result.startswith("ﻡﻼﺳ"))
        self.assertTrue(result.endswith("ﻥﺎﻬﺟ"))


if __name__ == "__main__":
    unittest.main(verbosity=2)