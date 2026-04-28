"""
parsikit - A pure Python library for Persian data formatting.

Modules:
    text:     Persian text standardization and normalization.
    number:   Digit conversion between Persian, Arabic, and English.
    currency: Currency formatting and unit conversion.
"""

from parsikit.text import standardize_persian
from parsikit.number import english_to_persian, persian_to_english
from parsikit.currency import format_currency, rial_to_toman

__version__ = "0.1.0"
__all__ = [
    "standardize_persian",
    "english_to_persian",
    "persian_to_english",
    "format_currency",
    "rial_to_toman",
]
