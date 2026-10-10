"""Unit tests for parsikit.dev module."""
import unittest
import parsikit
from parsikit.dev import (
    inspect_text, persian_repr, pformat, persian_fstring, validate_batch,
    pretty_print, setup_logging
)


class TestDevModule(unittest.TestCase):
    def test_inspect_text_empty(self):
        empty = inspect_text("")
        self.assertEqual(empty["length"], 0)
        self.assertEqual(empty["word_count"], 0)
        self.assertFalse(empty["is_persian"])

    def test_inspect_text_with_issues(self):
        bad_text = "ي كافيه  ك کتاب ها ميباشد 123"
        analysis = inspect_text(bad_text)
        self.assertTrue(analysis["has_arabic_chars"])
        self.assertTrue(analysis["has_english_digits"])
        self.assertTrue(analysis["has_zwnj_issues"])
        self.assertTrue(analysis["has_spacing_issues"])
        self.assertGreater(len(analysis["suggestions"]), 0)

    def test_inspect_text_clean(self):
        clean = "این یک متن استاندارد فارسی با نیم‌فاصله است."
        analysis = inspect_text(clean)
        self.assertFalse(analysis["has_arabic_chars"])
        self.assertFalse(analysis["has_zwnj_issues"])
        self.assertTrue(analysis["is_persian"])

    def test_inspect_text_persian_digits(self):
        persian_num_text = "شماره پلاک ۱۲۳"
        analysis = inspect_text(persian_num_text)
        self.assertTrue(analysis["has_persian_digits"])
        self.assertFalse(analysis["has_english_digits"])

    def test_persian_repr(self):
        data = {"نام": ["علی", "رضا"], "مشخصات": {"شهر": "تهران"}}
        rep = persian_repr(data)
        self.assertIn("نام", rep)
        self.assertIn("علی", rep)
        self.assertIn("رضا", rep)
        self.assertIn("تهران", rep)

    def test_pformat_alignment_and_persian_digits(self):
        # Alignment with ZWNJ
        zwnj_text = "کتاب\u200Cها"
        formatted = pformat("{:<10}", zwnj_text)
        self.assertEqual(len(formatted), 11)
        self.assertTrue(formatted.endswith("   "))

        # Diacritics
        diacritic_text = "سَلام"
        formatted_diac = pformat("{:<10}", diacritic_text)
        self.assertEqual(len(formatted_diac), 11)
        self.assertTrue(formatted_diac.endswith("      "))

        # Persian digits format suffix :fa and :p
        self.assertEqual(pformat("{:fa}", 15000), "۱۵۰۰۰")
        self.assertEqual(pformat("{:p}", 15000), "۱۵۰۰۰")
        self.assertEqual(pformat("{:>10,fa}", 15000), "    ۱۵،۰۰۰")

    def test_persian_fstring(self):
        name = "علی"
        age = 28
        price = 15000000

        res = persian_fstring("نام: {name:<5} | سن: {age:fa} | قیمت: {price:,fa} ریال")
        self.assertEqual(res, "نام: علی   | سن: ۲۸ | قیمت: ۱۵،۰۰۰،۰۰۰ ریال")

        res_override = persian_fstring("نام: {name}", name="رضا")
        self.assertEqual(res_override, "نام: رضا")

    def test_validate_batch(self):
        items = ["7730123452", "1111111111", "0010123458", "invalid-code"]
        report = validate_batch(items, parsikit.NationalCode, silent=True)
        self.assertEqual(report["total"], 4)
        self.assertEqual(report["valid_count"], 2)
        self.assertEqual(report["invalid_count"], 2)
        self.assertEqual(len(report["errors"]), 2)
        self.assertEqual(report["errors"][0]["index"], 1)

    def test_pretty_print_runs(self):
        sample = {"کاربر": "علی", "شناسه": 105, "فعال": True}
        # Runs without crashing
        pretty_print(sample, title="تست پرینتر", color=False)

    def test_setup_logging(self):
        logger = setup_logging("INFO")
        self.assertEqual(logger.name, "parsikit")


if __name__ == "__main__":
    unittest.main()
