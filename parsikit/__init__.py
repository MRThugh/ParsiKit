"""
parsikit
~~~~~~~~
A pure Python library for Persian data formatting, validation, and normalization.
"""

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

__version__ = "2.1.0"
__all__ = [
    # text
    "standardize_persian",
    "strip_diacritics",
    "is_persian",
    "correct_keyboard_layout",
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
    # reshaper
    "reshape_for_graphics",
]