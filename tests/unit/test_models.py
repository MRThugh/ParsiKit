"""Unit tests for parsikit.models module."""
import unittest
import parsikit
from parsikit.models import (
    PersianText, NationalCode, MobileNumber, FixedLine, BankCard, Sheba, VehiclePlate
)
from parsikit.exceptions import (
    InvalidNationalCodeError, InvalidMobileError, InvalidCardNumberError,
    InvalidShebaError, InvalidPlateError
)


class TestModelsModule(unittest.TestCase):
    def test_persian_text_model(self):
        text = PersianText("ي كافيه ك")
        self.assertEqual(str(text.standardize()), "ی کافیه ک")

        t1 = PersianText("سلام")
        t2 = PersianText("جهان")
        result = t1 + " " + t2
        self.assertEqual(str(result), "سلام جهان")
        self.assertIsInstance(result, PersianText)
        self.assertEqual(len(result), 9)
        self.assertEqual(result.raw, "سلام جهان")

    def test_national_code_model(self):
        with self.assertRaises(InvalidNationalCodeError):
            NationalCode("1111111111")

        nc = NationalCode("7730123452")
        self.assertEqual(nc.clean, "7730123452")
        self.assertEqual(nc.formatted, "773-012345-2")
        self.assertEqual(nc.masked, "773-****45-2")
        self.assertTrue(nc.is_valid)
        self.assertEqual(len(nc), 10)
        self.assertEqual(nc, "7730123452")

        # Loose validation mode
        nc_loose = NationalCode("1111111111", strict=False)
        self.assertFalse(nc_loose.is_valid)

        # Prefix/Location detection test with valid Tehran code
        nc_tehran = NationalCode("0010123458")
        self.assertIsNotNone(nc_tehran.location)
        self.assertEqual(nc_tehran.location["province"], "تهران")  # type: ignore

        # to_dict verification
        d = nc.to_dict()
        self.assertIn("masked", d)
        self.assertEqual(d["masked"], "773-****45-2")

    def test_mobile_number_model(self):
        with self.assertRaises(InvalidMobileError):
            MobileNumber("0912abc")

        mob = MobileNumber("+98۹۱۲۳۴۵۶۷۸۹")
        self.assertEqual(mob.to_national(), "09123456789")
        self.assertEqual(mob.to_international(), "+989123456789")
        self.assertEqual(mob.masked, "0912***6789")
        self.assertEqual(mob.operator, "MCI")
        self.assertTrue(mob.is_valid)

        d = mob.to_dict()
        self.assertIn("masked", d)
        self.assertEqual(d["masked"], "0912***6789")

    def test_fixed_line_model(self):
        fixed = FixedLine("02188888888")
        self.assertEqual(fixed.province, "تهران")
        self.assertEqual(fixed.area_code, "021")
        self.assertEqual(fixed.to_national(), "02188888888")
        self.assertEqual(fixed.to_international(), "+982188888888")
        self.assertTrue(fixed.is_valid)

    def test_bank_card_model(self):
        with self.assertRaises(InvalidCardNumberError):
            BankCard("1234")

        card = BankCard("6037991122334455")
        self.assertEqual(card.formatted, "6037-9911-2233-4455")
        self.assertEqual(card.masked, "6037-99**-****-4455")
        self.assertEqual(card.bank["code"], "melli")  # type: ignore
        self.assertTrue(card.is_valid)

        d = card.to_dict()
        self.assertIn("masked", d)
        self.assertEqual(d["masked"], "6037-99**-****-4455")

    def test_sheba_model(self):
        with self.assertRaises(InvalidShebaError):
            Sheba("IR000")

        sheba = Sheba("IR050170000000123456789012")
        self.assertEqual(sheba.bank["code"], "melli")  # type: ignore
        self.assertEqual(sheba.account_number, "123456789012")
        self.assertTrue(sheba.is_valid)

    def test_plate_model(self):
        with self.assertRaises(InvalidPlateError):
            VehiclePlate("invalid-plate")

        plate = VehiclePlate("۱۲ ب ۳۴۵ ایران ۶۸")
        self.assertEqual(plate.province, "البرز")
        self.assertEqual(plate.category, "شخصی")
        self.assertTrue(plate.is_valid)


if __name__ == "__main__":
    unittest.main()
