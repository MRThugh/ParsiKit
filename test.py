"""
Comprehensive test suite for the parsikit library.

Run with:
    python -m unittest discover -s tests
or simply:
    python -m pytest tests/
"""

import unittest

from parsikit.text import standardize_persian
from parsikit.number import english_to_persian, persian_to_english
from parsikit.currency import format_currency, rial_to_toman


# ===========================================================================
# text.py tests
# ===========================================================================

class TestStandardizePersian(unittest.TestCase):
    """Tests for parsikit.text.standardize_persian."""

    # --- Arabic character normalization ------------------------------------

    def test_arabic_yeh_to_persian_yeh(self):
        self.assertEqual(standardize_persian("ي"), "ی")

    def test_alef_maqsura_to_persian_yeh(self):
        self.assertEqual(standardize_persian("ى"), "ی")

    def test_arabic_kaf_to_persian_kaf(self):
        self.assertEqual(standardize_persian("ك"), "ک")

    def test_mixed_arabic_chars(self):
        self.assertEqual(standardize_persian("ي كتاب"), "ی کتاب")

    def test_arabic_indic_digits_normalized(self):
        # Arabic-Indic ١٢٣ → Persian ۱۲۳
        self.assertEqual(standardize_persian("١٢٣"), "۱۲۳")

    def test_already_persian_unchanged(self):
        text = "کتاب خوب"
        self.assertEqual(standardize_persian(text), text)

    # --- ZWNJ corrections --------------------------------------------------

    def test_mi_prefix_gets_zwnj(self):
        result = standardize_persian("می روم")
        self.assertIn("\u200C", result)
        self.assertEqual(result, "می\u200Cروم")

    def test_nami_prefix_gets_zwnj(self):
        result = standardize_persian("نمی دانم")
        self.assertEqual(result, "نمی\u200Cدانم")

    def test_bi_prefix_gets_zwnj(self):
        result = standardize_persian("بی توجه")
        self.assertEqual(result, "بی\u200Cتوجه")

    def test_ha_suffix_gets_zwnj(self):
        result = standardize_persian("کتاب ها")
        self.assertEqual(result, "کتاب\u200Cها")

    def test_haye_suffix_gets_zwnj(self):
        result = standardize_persian("کتاب های")
        self.assertEqual(result, "کتاب\u200Cهای")

    def test_am_suffix_gets_zwnj(self):
        result = standardize_persian("رفتم ام")
        self.assertEqual(result, "رفتم\u200Cام")

    # --- Whitespace normalization ------------------------------------------

    def test_multiple_spaces_collapsed(self):
        self.assertEqual(standardize_persian("سلام   دنیا"), "سلام دنیا")

    def test_leading_trailing_stripped(self):
        self.assertEqual(standardize_persian("  سلام  "), "سلام")

    # --- Edge cases --------------------------------------------------------

    def test_empty_string(self):
        self.assertEqual(standardize_persian(""), "")

    def test_none_like_falsy_passthrough(self):
        # Empty string is falsy → returned as-is
        self.assertEqual(standardize_persian(""), "")

    def test_numbers_and_text_mixed(self):
        result = standardize_persian("١٢٣ ي كتاب")
        self.assertEqual(result, "۱۲۳ ی کتاب")


# ===========================================================================
# number.py tests
# ===========================================================================

class TestEnglishToPersian(unittest.TestCase):
    """Tests for parsikit.number.english_to_persian."""

    def test_single_digit(self):
        self.assertEqual(english_to_persian("5"), "۵")

    def test_full_digit_range(self):
        self.assertEqual(english_to_persian("0123456789"), "۰۱۲۳۴۵۶۷۸۹")

    def test_mixed_text_and_digits(self):
        self.assertEqual(english_to_persian("Order 42"), "Order ۴۲")

    def test_arabic_indic_to_persian(self):
        self.assertEqual(english_to_persian("١٢٣"), "۱۲۳")

    def test_already_persian_unchanged(self):
        self.assertEqual(english_to_persian("۱۲۳"), "۱۲۳")

    def test_empty_string(self):
        self.assertEqual(english_to_persian(""), "")

    def test_no_digits_unchanged(self):
        self.assertEqual(english_to_persian("hello"), "hello")

    def test_large_number(self):
        self.assertEqual(english_to_persian("1000000"), "۱۰۰۰۰۰۰")


class TestPersianToEnglish(unittest.TestCase):
    """Tests for parsikit.number.persian_to_english."""

    def test_single_digit(self):
        self.assertEqual(persian_to_english("۵"), "5")

    def test_full_persian_range(self):
        self.assertEqual(persian_to_english("۰۱۲۳۴۵۶۷۸۹"), "0123456789")

    def test_arabic_indic_to_english(self):
        self.assertEqual(persian_to_english("٠١٢٣٤٥٦٧٨٩"), "0123456789")

    def test_mixed_text_and_digits(self):
        self.assertEqual(persian_to_english("قیمت: ۱۲۳۴"), "قیمت: 1234")

    def test_already_english_unchanged(self):
        self.assertEqual(persian_to_english("1234"), "1234")

    def test_empty_string(self):
        self.assertEqual(persian_to_english(""), "")

    def test_roundtrip(self):
        original = "9876543210"
        self.assertEqual(persian_to_english(english_to_persian(original)), original)


# ===========================================================================
# currency.py tests
# ===========================================================================

class TestFormatCurrency(unittest.TestCase):
    """Tests for parsikit.currency.format_currency."""

    def test_basic_toman(self):
        self.assertEqual(format_currency(1000000), "1,000,000 تومان")

    def test_basic_rial(self):
        self.assertEqual(format_currency(1000000, "rial"), "1,000,000 ریال")

    def test_string_input(self):
        self.assertEqual(format_currency("500000"), "500,000 تومان")

    def test_persian_digit_string_input(self):
        self.assertEqual(format_currency("۱۵۰۰۰۰"), "150,000 تومان")

    def test_arabic_indic_string_input(self):
        self.assertEqual(format_currency("١٥٠٠٠٠"), "150,000 تومان")

    def test_persian_digits_output(self):
        result = format_currency(1000000, persian_digits=True)
        self.assertEqual(result, "۱،۰۰۰،۰۰۰ تومان")

    def test_zero_amount(self):
        self.assertEqual(format_currency(0), "0 تومان")

    def test_small_amount(self):
        self.assertEqual(format_currency(500), "500 تومان")

    def test_currency_case_insensitive(self):
        self.assertEqual(
            format_currency(1000, "TOMAN"), format_currency(1000, "toman")
        )

    def test_invalid_currency_raises(self):
        with self.assertRaises(ValueError):
            format_currency(1000, "dollar")

    def test_invalid_amount_raises(self):
        with self.assertRaises(ValueError):
            format_currency("not_a_number")

    def test_large_amount(self):
        self.assertEqual(format_currency(1_000_000_000), "1,000,000,000 تومان")


class TestRialToToman(unittest.TestCase):
    """Tests for parsikit.currency.rial_to_toman."""

    def test_exact_conversion(self):
        self.assertEqual(rial_to_toman(10000), 1000)

    def test_truncation(self):
        # 15 Rial → 1 Toman (integer division)
        self.assertEqual(rial_to_toman(15), 1)

    def test_zero(self):
        self.assertEqual(rial_to_toman(0), 0)

    def test_single_rial(self):
        self.assertEqual(rial_to_toman(9), 0)

    def test_negative_raises(self):
        with self.assertRaises(ValueError):
            rial_to_toman(-100)

    def test_large_amount(self):
        self.assertEqual(rial_to_toman(1_000_000_000), 100_000_000)


# ===========================================================================
# Integration tests
# ===========================================================================

class TestIntegration(unittest.TestCase):
    """End-to-end scenarios combining multiple modules."""

    def test_user_input_pipeline(self):
        """Simulate a typical user input: Arabic text + Persian price."""
        raw_text = "ي كتاب"
        raw_price = "۱۵۰۰۰۰"

        clean_text = standardize_persian(raw_text)
        price_int = int(persian_to_english(raw_price))
        formatted = format_currency(price_int)

        self.assertEqual(clean_text, "ی کتاب")
        self.assertEqual(price_int, 150000)
        self.assertEqual(formatted, "150,000 تومان")

    def test_rial_input_to_formatted_toman(self):
        """Convert a Rial amount to Toman and format it."""
        rial_amount = 5_000_000
        toman = rial_to_toman(rial_amount)
        result = format_currency(toman, persian_digits=True)
        self.assertEqual(result, "۵۰۰،۰۰۰ تومان")

    def test_full_normalization_then_display(self):
        """Normalize Arabic input, convert digits, format for display."""
        raw = "قيمت: 1500000 ريال"
        normalized = standardize_persian(raw)
        # Extract and convert the number
        digits_only = "".join(c for c in normalized if c.isdigit())
        formatted = format_currency(int(digits_only), "rial", persian_digits=True)
        self.assertIn("ریال", formatted)
        self.assertIn("۱،۵۰۰،۰۰۰", formatted)


if __name__ == "__main__":
    unittest.main(verbosity=2)
