"""
Comprehensive test suite for ParsiKit version 3.3.0.
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
        # Checking that dict serialization matches expectations (Corrected typo from "account" to "account_number")
        data = {
            "iban": str(sheba),
            "bank_name": sheba.bank["name"] if sheba.bank else None,
            "account_number": sheba.account_number
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


class TestDeveloperUtilityV330(unittest.TestCase):
    def test_inspect_text(self):
        # Test empty input handling
        empty_analysis = parsikit.inspect_text("")
        self.assertEqual(empty_analysis["length"], 0)
        self.assertEqual(empty_analysis["word_count"], 0)

        # Test text with common Persian layout/spacing/character errors
        bad_text = "ي كافيه ك کتاب ها ميباشد ۱۲۳"
        analysis = parsikit.inspect_text(bad_text)
        
        self.assertTrue(analysis["has_arabic_chars"])
        self.assertTrue(analysis["has_english_digits"])
        self.assertTrue(analysis["has_zwnj_issues"])
        self.assertTrue(analysis["has_spacing_issues"])
        self.assertGreater(len(analysis["suggestions"]), 0)

        # Test valid standard Persian text
        clean_text = "این یک متن استاندارد فارسی با نیم‌فاصله است."
        clean_analysis = parsikit.inspect_text(clean_text)
        self.assertFalse(clean_analysis["has_arabic_chars"])
        self.assertFalse(clean_analysis["has_zwnj_issues"])

    def test_persian_repr(self):
        # Standard Python output escapes Persian characters, persian_repr shouldn't.
        data = {"نام": ["علی", "رضا"]}
        representation = parsikit.persian_repr(data)
        
        self.assertIn("نام", representation)
        self.assertIn("علی", representation)
        self.assertIn("رضا", representation)

    def test_validate_batch(self):
        # Validate batch lists containing both valid and invalid national codes
        items = ["7730123452", "1111111111", "0010123451", "invalid-code"]
        report = parsikit.validate_batch(items, parsikit.NationalCode, silent=True)

        self.assertEqual(report["total"], 4)
        self.assertEqual(report["valid_count"], 2)
        self.assertEqual(report["invalid_count"], 2)
        self.assertEqual(len(report["errors"]), 2)
        self.assertEqual(report["errors"][0]["index"], 1)

    def test_pretty_print_runs(self):
        # Ensure pretty printer processes structures without crashing
        sample_dict = {"کاربر": "علی", "شناسه": 105, "فعال": True}
        try:
            parsikit.pretty_print(sample_dict, title="تست پرینتر", color=False)
        except Exception as e:
            self.fail(f"pretty_print raised an unexpected error: {e}")

    def test_pformat_and_persian_aware_alignment(self):
        # Test standard python vs persian_aware visual alignment with ZWNJ (zero-width)
        zwnj_text = "کتاب‌‌ها"
        formatted = parsikit.pformat("{:<10}", zwnj_text)
        self.assertEqual(len(formatted), 11)
        self.assertTrue(formatted.endswith("   "))

        # Test diacritics formatting
        diacritic_text = "سَلام"
        formatted_diac = parsikit.pformat("{:<10}", diacritic_text)
        self.assertEqual(len(formatted_diac), 11)
        self.assertTrue(formatted_diac.endswith("      "))

        # Test Persian digit suffix ':fa' and ':p'
        self.assertEqual(parsikit.pformat("{:fa}", 15000), "۱۵۰۰۰")
        self.assertEqual(parsikit.pformat("{:p}", 15000), "۱۵۰۰۰")
        self.assertEqual(parsikit.pformat("{:>10,fa}", 15000), "    ۱۵،۰۰۰")

    def test_persian_fstring_capturing(self):
        name = "علی"
        age = 28
        price = 15000000
        
        result = parsikit.persian_fstring("نام: {name:<5} | سن: {age:fa} | قیمت: {price:,fa} ریال")
        self.assertEqual(result, "نام: علی   | سن: ۲۸ | قیمت: ۱۵،۰۰۰،۰۰۰ ریال")

        result_override = parsikit.persian_fstring("نام: {name}", name="رضا")
        self.assertEqual(result_override, "نام: رضا")

    def test_slugify(self):
        # Test standard Persian-to-Finglish Romanization
        self.assertEqual(parsikit.slugify("سلام دنیا"), "salam-donya")
        
        # Test dictionaries mapping for popular terms
        self.assertEqual(parsikit.slugify("آموزش وردپرس"), "amoozesh-wordpress")
        
        # Test mixture with english variables and numbers
        self.assertEqual(parsikit.slugify("سایت WordPress نسخه 6"), "site-wordpress-neskheh-6")

    def test_clean_text(self):
        dirty_input = "ي كافيه ك   کتاب  ها  ميباشد  ۱۱۲۳\n\n\n\nجدید  "
        cleaned_output = parsikit.clean_text(dirty_input)
        
        # Expected conversions:
        # ي -> ی, ك -> ک, ميباشد -> میباشد (standardize)
        # spaces collapsed, semi-space (ZWNJ) formatted
        # newlines collapsed, english-style numbers -> Persian digits
        self.assertIn("کتاب‌ها", cleaned_output)
        self.assertIn("میباشد", cleaned_output)
        self.assertIn("۱۱۲۳", cleaned_output)
        self.assertIn("\n\nجدید", cleaned_output)

    def test_normalize_whitespace(self):
        # Test basic spaces normalization
        self.assertEqual(parsikit.normalize_whitespace("  سلام   دنیا  "), "سلام دنیا")

        # Test line spacing and empty lines collapsing (keep_paragraphs=True)
        raw_paragraphs = "خط اول\n\n\n\nخط دوم   با   فاصله\n\nخط سوم"
        expected_paragraphs = "خط اول\n\nخط دوم با فاصله\n\nخط سوم"
        self.assertEqual(parsikit.normalize_whitespace(raw_paragraphs), expected_paragraphs)

        # Test flattening (keep_paragraphs=False)
        self.assertEqual(parsikit.normalize_whitespace(raw_paragraphs, keep_paragraphs=False), "خط اول خط دوم با فاصله خط سوم")

        # Test zero-width non-joiner preservation (must not be collapsed to standard space)
        self.assertEqual(parsikit.normalize_whitespace("کتاب\u200Cها   زیبا   هستند"), "کتاب\u200Cها زیبا هستند")

    def test_convert_numbers(self):
        # Convert English/Arabic numbers to Persian digits
        self.assertEqual(parsikit.convert_numbers("Price: 12500 USD", "persian"), "Price: ۱۲۵۰۰ USD")
        self.assertEqual(parsikit.convert_numbers("تلفن: 09123456789", "persian"), "تلفن: ۰۹۱۲۳۴۵۶۷۸۹")

        # Convert Persian/Arabic numbers to English digits
        self.assertEqual(parsikit.convert_numbers("قیمت: ۱۲۵۰۰ ریال", "english"), "قیمت: 12500 ریال")
        self.assertEqual(parsikit.convert_numbers("کد: ۰۹۱۲", "english"), "کد: 0912")

        # Test default parameter (defaults to "persian")
        self.assertEqual(parsikit.convert_numbers("123"), "۱۲۳")

        # Ensure ValueError is raised on unsupported style choice
        with self.assertRaises(ValueError):
            parsikit.convert_numbers("123", "french")

    def test_detect_data_types(self):
        # Test Mobile Numbers (English and Persian digit script)
        self.assertEqual(parsikit.detect("09123456789"), "mobile_number")
        self.assertEqual(parsikit.detect("+98۹۱۲۳۴۵۶۷۸۹"), "mobile_number")

        # Test National Codes (clean and formatted layouts)
        self.assertEqual(parsikit.detect("773-012345-2"), "national_code")
        self.assertEqual(parsikit.detect("7730123452"), "national_code")

        # Test Bank Cards
        self.assertEqual(parsikit.detect("6037-9911-2233-4455"), "bank_card")
        self.assertEqual(parsikit.detect("6037991122334455"), "bank_card")

        # Test Sheba codes (clean and spaced styles)
        self.assertEqual(parsikit.detect("IR050170000000123456789012"), "sheba")
        self.assertEqual(parsikit.detect("IR05 0170 0000 0012 3456 7890 12"), "sheba")

        # Test Emails
        self.assertEqual(parsikit.detect("user.name+test@subdomain.domain.com"), "email")

        # Test URLs
        self.assertEqual(parsikit.detect("https://parsikit.ir/docs"), "url")
        self.assertEqual(parsikit.detect("http://localhost:8080/v1/api"), "url")

        # Test IP addresses (IPv4 & IPv6 structures)
        self.assertEqual(parsikit.detect("192.168.1.1"), "ip")
        self.assertEqual(parsikit.detect("2001:0db8:85a3:0000:0000:8a2e:0370:7334"), "ip")

        # Test fallback scenarios
        self.assertIsNone(parsikit.detect("plain random text string"))
        self.assertIsNone(parsikit.detect(""))

    def test_mask_utilities(self):
        # Test mobile masking (Iranian standard format)
        self.assertEqual(parsikit.mask_mobile("09123456789"), "0912***6789")
        self.assertEqual(parsikit.mask_mobile("+989123456789"), "0912***6789")
        self.assertEqual(parsikit.mask_mobile("09123456789", mask_char="X"), "0912XXX6789")

        # Test card masking (Luhn validation preserved, beautifully formatted chunks)
        self.assertEqual(parsikit.mask_card("6037-9911-2233-4455"), "6037-99**-****-4455")
        self.assertEqual(parsikit.mask_card("6037991122334455"), "6037-99**-****-4455")
        self.assertEqual(parsikit.mask_card("6037991122334455", mask_char="X"), "6037-99XX-XXXX-4455")

        # Test national code masking (Formatted to standard layout)
        self.assertEqual(parsikit.mask_national_code("7730123452"), "773-****45-2")
        self.assertEqual(parsikit.mask_national_code("773-012345-2"), "773-****45-2")
        self.assertEqual(parsikit.mask_national_code("7730123452", mask_char="X"), "773-XXXX45-2")

        # Test email masking
        self.assertEqual(parsikit.mask_email("ali@example.com"), "al***i@example.com")
        self.assertEqual(parsikit.mask_email("kamrani.exe@gmail.com"), "ka******e@gmail.com")
        self.assertEqual(parsikit.mask_email("ax@example.com"), "a*@example.com")


if __name__ == "__main__":
    unittest.main(verbosity=2)