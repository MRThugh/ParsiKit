"""
Comprehensive test suite for ParsiKit version 2.8.0.
"""

import unittest

from parsikit.text import (
    standardize_persian,
    strip_diacritics,
    is_persian,
    correct_keyboard_layout,
    persian_sort_key,
    persian_sorted,
    beautify_persian_spacing,
)
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
    is_valid_corporate_id,
    detect_mobile_operator,
    detect_bank_from_card,
    detect_bank_from_sheba,
    is_valid_postal_code,
    format_postal_code,
    is_valid_bill_and_payment,
    extract_bill_details,
    is_valid_plate,
    parse_plate,
    format_plate,
)
from parsikit.datetime import (
    gregorian_to_jalali,
    jalali_to_gregorian,
    format_jalali,
)
from parsikit.reshaper import (
    reshape_for_graphics,
    reshape_paragraph_for_graphics,
)
from parsikit.gui import (
    _format_national_code,
    _format_card_number,
    _format_postal_code,
    _format_sheba,
)


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
        self.assertTrue(is_persian("ﻡﻼﺳ"))

    def test_correct_keyboard_layout(self):
        self.assertEqual(correct_keyboard_layout("sghl"), "سلام")
        self.assertEqual(correct_keyboard_layout("sghl?"), "سلام؟")
        self.assertEqual(correct_keyboard_layout("Hvn"), "آرد")
        self.assertEqual(correct_keyboard_layout("c\\"), "زژ")

    def test_persian_collation_sorting(self):
        items = ["گوسفند", "پروانه", "سيب", "ژاله", "آسمان", "باد", "خرس", "یاس"]
        correct_order = ["آسمان", "باد", "پروانه", "خرس", "ژاله", "سيب", "گوسفند", "یاس"]
        self.assertEqual(sorted(items, key=persian_sort_key), correct_order)

        mixed_items = ["گوسفند", "Apple", "123", "سیب", "۱۲", "آسمان", "Banana"]
        expected_mixed = ["۱۲", "123", "Apple", "Banana", "آسمان", "سیب", "گوسفند"]
        self.assertEqual(persian_sorted(mixed_items), expected_mixed)

    def test_beautify_persian_spacing(self):
        self.assertEqual(
            beautify_persian_spacing("سلام , چطوری ؟ من خوبم."),
            "سلام، چطوری؟ من خوبم."
        )
        self.assertEqual(
            beautify_persian_spacing("سیب,گلابی,پرتقال"),
            "سیب، گلابی، پرتقال"
        )
        self.assertEqual(
            beautify_persian_spacing("امروز ( شنبه ) فردا(یکشنبه) است."),
            "امروز (شنبه) فردا (یکشنبه) است."
        )


class TestNumber(unittest.TestCase):
    def test_conversions(self):
        self.assertEqual(english_to_persian("987"), "۹۸۷")
        self.assertEqual(persian_to_english("۹۸۷"), "987")

    def test_to_words(self):
        self.assertEqual(number_to_words(0), "صفر")
        self.assertEqual(number_to_words("۱۲۵۰۰"), "دوازده هزار و پانصد")
        self.assertEqual(number_to_words(-12), "منفی دوازده")
        self.assertEqual(number_to_words("۱,۲۵۰,۰۰۰"), "یک میلیون و دویست و پنجاه هزار")
        self.assertEqual(number_to_words("10,000,000,000,000,000,000"), "ده کوئینتیلیون")
        with self.assertRaises(ValueError):
            number_to_words("1" * 30)


class TestCurrency(unittest.TestCase):
    def test_formatting(self):
        self.assertEqual(format_currency(5000000), "5,000,000 تومان")
        self.assertEqual(format_currency(500000, persian_digits=True), "۵۰۰،۰۰۰ تومان")
        self.assertEqual(format_currency("1,200,500"), "1,200,500 تومان")

    def test_conversions(self):
        self.assertEqual(rial_to_toman(10), 1)
        self.assertEqual(toman_to_rial(1), 10)

    def test_words(self):
        self.assertEqual(format_currency_to_words(1000000, "toman"), "یک میلیون تومان")
        self.assertEqual(format_currency_to_words("1,500,000", "toman"), "یک میلیون و پانصد هزار تومان")

    def test_tax(self):
        self.assertEqual(add_tax_and_toll(100000), 110000)
        self.assertEqual(add_tax_and_toll("100,000"), 110000)

    def test_installments(self):
        self.assertEqual(calculate_installments(10000000, 18.0, 12), 916799)
        self.assertEqual(calculate_installments("10,000,000", 18.0, 12), 916799)


class TestValidators(unittest.TestCase):
    def test_national_code(self):
        self.assertTrue(is_valid_national_code("7730123452"))
        self.assertFalse(is_valid_national_code("1111111111"))
        self.assertEqual(format_national_code("7730123452"), "773-012345-2")
        self.assertTrue(is_valid_national_code("773012346"))

    def test_corporate_id(self):
        self.assertTrue(is_valid_corporate_id("14003632892"))
        self.assertTrue(is_valid_corporate_id("14010212749"))
        self.assertFalse(is_valid_corporate_id("11111111111"))
        self.assertFalse(is_valid_corporate_id("14010212748"))

    def test_mobile(self):
        self.assertTrue(is_valid_mobile("+98۹۱۲۳۴۵۶۷۸۹"))
        self.assertEqual(normalize_mobile("09123456789", prefix="+98"), "+989123456789")
        self.assertEqual(normalize_mobile("09123456789", prefix="0098"), "00989123456789")
        self.assertEqual(normalize_mobile("09123456789", prefix=""), "9123456789")

    def test_detect_operator(self):
        self.assertEqual(detect_mobile_operator("09121112233"), "MCI")
        self.assertEqual(detect_mobile_operator("+989351234567"), "Irancell")
        self.assertEqual(detect_mobile_operator("00989211234567"), "RighTel")
        self.assertEqual(detect_mobile_operator("09981234567"), "Shatel Mobile")
        self.assertEqual(detect_mobile_operator("09991234567"), "SamanTel")
        self.assertEqual(detect_mobile_operator("invalid"), None)

    def test_bank_card(self):
        self.assertTrue(is_valid_card_number("6037991122334455"))
        self.assertEqual(format_card_number("6037991122334455"), "6037-9911-2233-4455")

    def test_detect_bank_from_card(self):
        melli_bank = detect_bank_from_card("6037991122334455")
        self.assertEqual(melli_bank["code"], "melli")
        self.assertEqual(melli_bank["name"], "بانک ملی ایران")

        mellat_bank = detect_bank_from_card("610433")
        self.assertEqual(mellat_bank["code"], "mellat")

        self.assertIsNone(detect_bank_from_card("111111"))

    def test_sheba(self):
        self.assertTrue(is_valid_sheba("IR050170000000123456789012"))
        self.assertEqual(
            format_sheba("050170000000123456789012"),
            "IR05 0170 0000 0012 3456 7890 12"
        )
        self.assertTrue(is_valid_sheba("IR-05 0170 0000 0012 3456 7890 12"))

    def test_detect_bank_from_sheba(self):
        melli_bank = detect_bank_from_sheba("IR050170000000123456789012")
        self.assertEqual(melli_bank["code"], "melli")

        mellat_bank = detect_bank_from_sheba("050120000000123456789012")
        self.assertEqual(mellat_bank["code"], "mellat")

        self.assertIsNone(detect_bank_from_sheba("IR0519"))

    def test_postal_code(self):
        self.assertTrue(is_valid_postal_code("1453902410"))
        self.assertEqual(format_postal_code("1453902410"), "14539-02410")
        self.assertFalse(is_valid_postal_code("1453202410"))

    def test_bill_and_payment_id(self):
        bill_id = "7748317800142"
        pay_id = "1770160"
        self.assertTrue(is_valid_bill_and_payment(bill_id, pay_id))
        
        details = extract_bill_details(bill_id, pay_id)
        self.assertTrue(details["is_valid"])
        self.assertEqual(details["type"], "تلفن ثابت")
        self.assertEqual(details["amount_rial"], 17701000)
        self.assertEqual(details["amount_toman"], 1770100)

    def test_vehicle_plates(self):
        # 68 is Alborz
        plate = "۱۲ ب ۳۴۵ ایران ۶۸"
        self.assertTrue(is_valid_plate(plate))
        
        parsed = parse_plate(plate)
        self.assertEqual(parsed["part1"], "۱۲")
        self.assertEqual(parsed["letter"], "ب")
        self.assertEqual(parsed["province"], "البرز")
        self.assertEqual(parsed["category"], "شخصی")
        
        # Format checks
        self.assertEqual(format_plate(plate), "۱۲ ب ۳۴۵ - ایران ۶۸")
        self.assertEqual(format_plate("12الف34568", format_type="clean"), "۱۲الف۳۴۵۶۸")


class TestDatetime(unittest.TestCase):
    def test_conversions(self):
        jy, jm, jd = gregorian_to_jalali(2026, 7, 5)
        self.assertEqual((jy, jm, jd), (1405, 4, 14))

        gy, gm, gd = jalali_to_gregorian(1405, 4, 14)
        self.assertEqual((gy, gm, gd), (2026, 7, 5))

    def test_formatting(self):
        formatted = format_jalali(1405, 4, 14, "YYYY/MM/DD")
        self.assertEqual(formatted, "1405/04/14")

        formatted_dash = format_jalali(1405, 4, 14, "YYYY-MM-DD")
        self.assertEqual(formatted_dash, "1405-04-14")


class TestReshaper(unittest.TestCase):
    def test_basic_reshaping(self):
        shaped_reversed = reshape_for_graphics("سلام")
        self.assertEqual(shaped_reversed, "ﻡﻼﺳ")

    def test_diacritics_connectivity(self):
        shaped = reshape_for_graphics("عَلِیّ", reverse=False)
        self.assertEqual(shaped, "ﻋَﻠِﻲّ")

    def test_mixed_reshaping(self):
        result = reshape_for_graphics("سلام Hello جهان")
        self.assertIn("Hello", result)
        self.assertTrue(result.startswith("ﻡﻼﺳ"))
        self.assertTrue(result.endswith("ﻥﺎﻬﺟ"))

    def test_arabic_ligatures_reshaping(self):
        shaped = reshape_for_graphics("تأثیر")
        expected = "\uFEAE\uFEF4\uFE9B\uFE84\uFE97"
        self.assertEqual(shaped, expected)

    def test_paragraph_wrapping(self):
        paragraph = "سلام جهان این یک متن بسیار طولانی برای تست بسته بندی خودکار خطوط فارسی است"
        lines = reshape_paragraph_for_graphics(paragraph, 20, reverse=True)
        self.assertEqual(len(lines), 4)
        self.assertTrue(lines[0].startswith("ﻡﻼﺳ"))


class TestGuiFormatters(unittest.TestCase):
    def test_national_code_formatter(self):
        self.assertEqual(_format_national_code("7730123452"), "773-012345-2")
        self.assertEqual(_format_national_code("7730"), "773-0")

    def test_card_formatter(self):
        self.assertEqual(_format_card_number("6037991122334455"), "6037-9911-2233-4455")
        self.assertEqual(_format_card_number("603799"), "6037-99")

    def test_postal_code_formatter(self):
        self.assertEqual(_format_postal_code("1453902410"), "14539-02410")

    def test_sheba_formatter(self):
        self.assertEqual(_format_sheba("ir05017"), "IR05 017")
        self.assertEqual(_format_sheba("05017"), "IR05 017")


if __name__ == "__main__":
    unittest.main(verbosity=2)