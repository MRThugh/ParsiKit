"""
Comprehensive test suite for ParsiKit version 3.2.0.
"""

import unittest
import datetime

import parsikit
from parsikit.exceptions import (
    InvalidNationalCodeError, InvalidMobileError, InvalidCardNumberError,
    InvalidShebaError, InvalidPlateError, ValidationError
)


class TestInfrastructureOOP(unittest.TestCase):
    def setUp(self) -> None:
        parsikit.config.reset_defaults()

    def test_persian_text_model(self):
        text = parsikit.PersianText("ي كافيه ك")
        self.assertEqual(str(text.standardize()), "ی کافیه ک")
        
        # Test addition and concatenation
        t1 = parsikit.PersianText("سلام")
        t2 = parsikit.PersianText("جهان")
        result = t1 + " " + t2
        self.assertEqual(str(result), "سلام جهان")
        self.assertIsInstance(result, parsikit.PersianText)

    def test_national_code_model(self):
        with self.assertRaises(InvalidNationalCodeError):
            parsikit.NationalCode("1111111111")
            
        nc = parsikit.NationalCode("7730123452")
        self.assertEqual(nc.clean, "7730123452")
        self.assertEqual(nc.formatted, "773-012345-2")
        self.assertTrue(nc.is_valid)

        # Loose validation
        nc_loose = parsikit.NationalCode("1111111111", strict=False)
        self.assertFalse(nc_loose.is_valid)

        # Prefix/Location detection test
        nc_tehran = parsikit.NationalCode("0010123451")
        self.assertIsNotNone(nc_tehran.location)
        self.assertEqual(nc_tehran.location["province"], "تهران")  # type: ignore

    def test_mobile_number_model(self):
        with self.assertRaises(InvalidMobileError):
            parsikit.MobileNumber("0912abc")
            
        mob = parsikit.MobileNumber("+98۹۱۲۳۴۵۶۷۸۹")
        self.assertEqual(mob.to_national(), "09123456789")
        self.assertEqual(mob.to_international(), "+989123456789")
        self.assertEqual(mob.operator, "MCI")

    def test_bank_card_model(self):
        with self.assertRaises(InvalidCardNumberError):
            parsikit.BankCard("1234")
            
        card = parsikit.BankCard("6037991122334455")
        self.assertEqual(card.formatted, "6037-9911-2233-4455")
        self.assertEqual(card.bank["code"], "melli")

    def test_sheba_model(self):
        with self.assertRaises(InvalidShebaError):
            parsikit.Sheba("IR000")
            
        sheba = parsikit.Sheba("IR050170000000123456789012")
        self.assertEqual(sheba.bank["code"], "melli")
        self.assertEqual(sheba.account_number, "123456789012")

    def test_plate_model(self):
        with self.assertRaises(InvalidPlateError):
            parsikit.VehiclePlate("invalid-plate")
            
        plate = parsikit.VehiclePlate("۱۲ ب ۳۴۵ ایران ۶۸")
        self.assertEqual(plate.province, "البرز")
        self.assertEqual(plate.category, "شخصی")


class TestDeveloperExperienceV310(unittest.TestCase):
    def test_string_like_behavior_and_duck_typing(self):
        nc = parsikit.NationalCode("0010123451")
        # NationalCode works cleanly with standard python string functions and properties
        self.assertEqual(len(nc), 10)
        self.assertEqual(nc.clean[:3], "001")
        
        # Test equality with string
        self.assertEqual(nc, "0010123451")

    def test_dictionary_serialization(self):
        sheba = parsikit.Sheba("IR050170000000123456789012")
        # Checking that dict serialization matches expectations
        data = {
            "iban": str(sheba),
            "bank_name": sheba.bank["name"] if sheba.bank else None,
            "account": sheba.account_number
        }
        self.assertEqual(data["account_number"], "123456789012")  # type: ignore

    def test_fixed_landline_model(self):
        fixed = parsikit.FixedLine("02188888888")
        self.assertEqual(fixed.province, "تهران")
        self.assertEqual(fixed.area_code, "021")
        self.assertEqual(len(fixed), 11)


class TestNewFeaturesV310(unittest.TestCase):
    def test_words_to_number(self):
        self.assertEqual(parsikit.words_to_number("سی و دو هزار و پانصد"), 32500)
        self.assertEqual(parsikit.words_to_number("یک میلیون و دویست و پنجاه هزار"), 1250000)
        self.assertEqual(parsikit.words_to_number("منفی دوازده"), -12)
        
        text = parsikit.PersianText("سه میلیارد و پانصد میلیون")
        self.assertEqual(text.to_number(), 3500000000)

    def test_humanize_relative_time(self):
        ref = datetime.datetime(2026, 7, 6, 12, 0, 0)
        
        dt = datetime.datetime(2026, 7, 6, 11, 59, 55)
        self.assertEqual(parsikit.humanize_relative_time(dt, reference=ref), "هم‌اکنون")

        dt = datetime.datetime(2026, 7, 6, 11, 55, 0)
        self.assertEqual(parsikit.humanize_relative_time(dt, reference=ref), "۵ دقیقه پیش")

        dt = datetime.datetime(2026, 7, 6, 9, 0, 0)
        self.assertEqual(parsikit.humanize_relative_time(dt, reference=ref), "۳ ساعت پیش")

        dt = datetime.datetime(2026, 7, 5, 12, 0, 0)
        self.assertEqual(parsikit.humanize_relative_time(dt, reference=ref), "دیروز")

        dt = datetime.datetime(2026, 7, 1, 12, 0, 0)
        self.assertEqual(parsikit.humanize_relative_time(dt, reference=ref), "۵ روز پیش")


if __name__ == "__main__":
    unittest.main(verbosity=2)