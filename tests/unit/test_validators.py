"""Unit tests for parsikit.validators module."""
import unittest
from parsikit.validators import (
    is_valid_national_code, format_national_code, detect_national_code_location,
    is_valid_mobile, normalize_mobile, is_valid_landline, normalize_landline,
    detect_landline_province, is_valid_card_number, format_card_number,
    is_valid_sheba, format_sheba, extract_account_number_from_sheba,
    is_valid_corporate_id, detect_mobile_operator, detect_bank_from_card,
    detect_bank_from_sheba, is_valid_postal_code, format_postal_code,
    is_valid_bill_and_payment, extract_bill_details, is_valid_plate, parse_plate,
    format_plate, detect
)
from tests.fixtures.synthetic_data import (
    VALID_SYNTHETIC_NATIONAL_CODES, INVALID_NATIONAL_CODES,
    VALID_SYNTHETIC_MOBILES, INVALID_MOBILES,
    VALID_SYNTHETIC_BANK_CARDS, INVALID_BANK_CARDS,
    VALID_SYNTHETIC_SHEBAS, INVALID_SHEBAS,
    VALID_SYNTHETIC_PLATES, INVALID_PLATES
)


class TestValidatorsModule(unittest.TestCase):
    def test_national_code_validation(self):
        for code in VALID_SYNTHETIC_NATIONAL_CODES:
            self.assertTrue(is_valid_national_code(code), f"Expected valid: {code}")
        for code in INVALID_NATIONAL_CODES:
            self.assertFalse(is_valid_national_code(code), f"Expected invalid: {code}")
        self.assertFalse(is_valid_national_code(""))

    def test_format_national_code(self):
        self.assertEqual(format_national_code("7730123452"), "773-012345-2")
        self.assertEqual(format_national_code("12345"), "000-001234-5")
        with self.assertRaises(ValueError):
            format_national_code("123456789012")

    def test_detect_national_code_location(self):
        loc = detect_national_code_location("0010123458")
        self.assertIsNotNone(loc)
        self.assertEqual(loc["province"], "تهران")  # type: ignore

        loc_alborz = detect_national_code_location("0310123452")
        self.assertIsNotNone(loc_alborz)
        self.assertEqual(loc_alborz["province"], "البرز")  # type: ignore

        self.assertIsNone(detect_national_code_location("9990123452"))

    def test_mobile_validation_and_normalization(self):
        for phone in VALID_SYNTHETIC_MOBILES:
            self.assertTrue(is_valid_mobile(phone), f"Expected valid mobile: {phone}")
        for phone in INVALID_MOBILES:
            self.assertFalse(is_valid_mobile(phone), f"Expected invalid mobile: {phone}")

        self.assertEqual(normalize_mobile("09123456789", prefix="0"), "09123456789")
        self.assertEqual(normalize_mobile("09123456789", prefix="+98"), "+989123456789")
        self.assertEqual(normalize_mobile("09123456789", prefix=""), "9123456789")

    def test_detect_mobile_operator(self):
        self.assertEqual(detect_mobile_operator("09123456789"), "MCI")
        self.assertEqual(detect_mobile_operator("09351234567"), "Irancell")
        self.assertEqual(detect_mobile_operator("09201234567"), "RighTel")
        self.assertIsNone(detect_mobile_operator("invalid"))

    def test_landline_validation(self):
        self.assertTrue(is_valid_landline("02188888888"))
        self.assertTrue(is_valid_landline("+982188888888"))
        self.assertFalse(is_valid_landline("09123456789"))  # Mobile, not landline

        self.assertEqual(normalize_landline("02188888888", prefix="0"), "02188888888")
        self.assertEqual(detect_landline_province("02188888888"), "تهران")
        self.assertEqual(detect_landline_province("03133333333"), "اصفهان")

    def test_bank_card_validation(self):
        for card in VALID_SYNTHETIC_BANK_CARDS:
            self.assertTrue(is_valid_card_number(card), f"Expected valid card: {card}")
        for card in INVALID_BANK_CARDS:
            self.assertFalse(is_valid_card_number(card), f"Expected invalid card: {card}")

        self.assertEqual(format_card_number("6037991122334455"), "6037-9911-2233-4455")
        bank = detect_bank_from_card("6037991122334455")
        self.assertIsNotNone(bank)
        self.assertEqual(bank["code"], "melli")  # type: ignore

    def test_sheba_validation(self):
        for sheba in VALID_SYNTHETIC_SHEBAS:
            self.assertTrue(is_valid_sheba(sheba), f"Expected valid Sheba: {sheba}")
        for sheba in INVALID_SHEBAS:
            self.assertFalse(is_valid_sheba(sheba), f"Expected invalid Sheba: {sheba}")

        self.assertEqual(
            format_sheba("IR050170000000123456789012", format_type="spaced"),
            "IR05 0170 0000 0012 3456 7890 12"
        )
        self.assertEqual(
            extract_account_number_from_sheba("IR050170000000123456789012"),
            "123456789012"
        )
        bank = detect_bank_from_sheba("IR050170000000123456789012")
        self.assertIsNotNone(bank)
        self.assertEqual(bank["code"], "melli")  # type: ignore

    def test_corporate_id(self):
        # 11-digit legal entity national ID
        self.assertFalse(is_valid_corporate_id(""))
        self.assertFalse(is_valid_corporate_id("11111111111"))

    def test_postal_code(self):
        self.assertTrue(is_valid_postal_code("1345678912"))
        self.assertFalse(is_valid_postal_code("0123456789"))  # 0 in first 5 digits
        self.assertFalse(is_valid_postal_code("12345"))       # Length != 10

        self.assertEqual(format_postal_code("1345678912"), "13456-78912")

    def test_vehicle_plates(self):
        for plate in VALID_SYNTHETIC_PLATES:
            self.assertTrue(is_valid_plate(plate), f"Expected valid plate: {plate}")
        for plate in INVALID_PLATES:
            self.assertFalse(is_valid_plate(plate), f"Expected invalid plate: {plate}")

        parsed = parse_plate("۱۲ ب ۳۴۵ ایران ۶۸")
        self.assertIsNotNone(parsed)
        self.assertEqual(parsed["province"], "البرز")  # type: ignore
        self.assertEqual(parsed["category"], "شخصی")   # type: ignore

        self.assertEqual(format_plate("12ب34568", "readable"), "۱۲ ب ۳۴۵ - ایران ۶۸")

    def test_detect_utility(self):
        self.assertEqual(detect("09123456789"), "mobile_number")
        self.assertEqual(detect("7730123452"), "national_code")
        self.assertEqual(detect("6037991122334455"), "bank_card")
        self.assertEqual(detect("IR050170000000123456789012"), "sheba")
        self.assertEqual(detect("test@example.com"), "email")
        self.assertEqual(detect("https://example.com"), "url")
        self.assertEqual(detect("192.168.1.1"), "ip")
        self.assertIsNone(detect("just random text"))
        self.assertIsNone(detect(""))


if __name__ == "__main__":
    unittest.main()
