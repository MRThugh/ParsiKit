"""
parsikit
~~~~~~~~
A pure Python library for Persian data formatting, validation, and normalization.
"""

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
from parsikit.gui import bind_persian_input

__version__ = "2.8.0"
__all__ = [
    # text
    "standardize_persian",
    "strip_diacritics",
    "is_persian",
    "correct_keyboard_layout",
    "persian_sort_key",
    "persian_sorted",
    "beautify_persian_spacing",
    # number
    "english_to_persian",
    "persian_to_english",
    "number_to_words",
    # currency
    "format_currency",
    "rial_to_toman",
    "toman_to_rial",
    "format_currency_to_words",
    "add_tax_and_toll",
    "calculate_installments",
    # validators
    "is_valid_national_code",
    "format_national_code",
    "is_valid_mobile",
    "normalize_mobile",
    "is_valid_card_number",
    "format_card_number",
    "is_valid_sheba",
    "format_sheba",
    "is_valid_corporate_id",
    "detect_mobile_operator",
    "detect_bank_from_card",
    "detect_bank_from_sheba",
    "is_valid_postal_code",
    "format_postal_code",
    "is_valid_bill_and_payment",
    "extract_bill_details",
    "is_valid_plate",
    "parse_plate",
    "format_plate",
    # datetime
    "gregorian_to_jalali",
    "jalali_to_gregorian",
    "format_jalali",
    # reshaper
    "reshape_for_graphics",
    "reshape_paragraph_for_graphics",
    # gui
    "bind_persian_input",
]