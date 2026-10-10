"""Integration tests verifying multi-module OOP workflows in ParsiKit."""
import unittest
import parsikit


class TestOOPWorkflowIntegration(unittest.TestCase):
    def setUp(self):
        parsikit.config.reset_defaults()

    def test_text_to_domain_entities(self):
        raw_input = """
        کاربر جدید:
        نام: علي
        کد ملی: ۷۷۳۰۱۲۳۴۵۲
        شماره موبایل: ۰۹۱۲۳۴۵۶۷۸۹
        شماره کارت: ۶۰۳۷-۹۹۱۱-۲۲۳۳-۴۴۵۵
        مبلغ بیعانه: پانصد هزار تومان
        """
        # Step 1: Clean and standardize text
        cleaned = parsikit.clean_text(raw_input)
        self.assertIn("علی", cleaned)

        # Step 2: Extract structured entities
        mobiles = parsikit.extract_mobiles(cleaned)
        codes = parsikit.extract_national_codes(cleaned)
        self.assertEqual(len(mobiles), 1)
        self.assertEqual(len(codes), 1)

        # Step 3: Instantiate domain models
        mob = parsikit.MobileNumber(mobiles[0])
        nc = parsikit.NationalCode(codes[0])

        self.assertEqual(mob.operator, "MCI")
        self.assertEqual(nc.formatted, "773-012345-2")
        self.assertEqual(nc.masked, "773-****45-2")

        # Step 4: Parse words to currency
        amount = parsikit.words_to_number("پانصد هزار")
        self.assertEqual(amount, 500000)
        formatted_curr = parsikit.format_currency(amount, "toman", persian_digits=True)
        self.assertEqual(formatted_curr, "۵۰۰،۰۰۰ تومان")

    def test_jalali_accounting_workflow(self):
        # Calculate payment date in Jalali and loan installments
        principal = 120_000_000  # 120 million Rials
        monthly_payment = parsikit.calculate_installments(principal, annual_interest_rate=18.0, months=12)
        self.assertGreater(monthly_payment, 0)

        # Dates
        jy, jm, jd = parsikit.gregorian_to_jalali(2026, 7, 6)
        formatted_date = parsikit.format_jalali(jy, jm, jd)
        month_name = parsikit.get_jalali_month_name(jm)
        self.assertEqual(month_name, "تیر")
        self.assertEqual(formatted_date, "1405/04/15")


if __name__ == "__main__":
    unittest.main()
