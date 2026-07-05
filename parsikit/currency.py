"""
parsikit.currency
~~~~~~~~~~~~~~~~~
Monetary utilities, unit conversions, tax calculations, and loan installment planning.
"""

from __future__ import annotations
from parsikit.number import number_to_words

_CURRENCY_LABELS = {
    "toman": "تومان",
    "rial": "ریال",
}


def format_currency(
    amount: int | str,
    currency: str = "toman",
    *,
    persian_digits: bool = False,
) -> str:
    """Format a numeric amount as a readable currency with thousands separators (handles formatted inputs)."""
    currency = currency.lower()
    if currency not in _CURRENCY_LABELS:
        raise ValueError(f"Unknown currency '{currency}'")

    _persian_to_ascii = str.maketrans("۰۱۲۳۴۵۶۷۸۹٠١٢٣٤٥٦٧٨٩", "01234567890123456789")
    clean_amount = str(amount).replace(",", "").replace("،", "").replace(" ", "")
    normalized = clean_amount.translate(_persian_to_ascii)

    try:
        value = int(normalized)
    except ValueError:
        raise ValueError(f"Cannot convert '{amount}' to an integer amount.") from None

    label = _CURRENCY_LABELS[currency]

    if persian_digits:
        _to_persian = str.maketrans("0123456789,", "۰۱۲۳۴۵۶۷۸۹،")
        formatted = f"{value:,}".translate(_to_persian)
        return f"{formatted} {label}"

    return f"{value:,} {label}"


def rial_to_toman(amount: int) -> int:
    """Convert Iranian Rial to Toman."""
    if amount < 0:
        raise ValueError("Amount must be non-negative.")
    return amount // 10


def toman_to_rial(amount: int) -> int:
    """Convert Toman to Iranian Rial."""
    if amount < 0:
        raise ValueError("Amount must be non-negative.")
    return amount * 10


def format_currency_to_words(amount: int | str, currency: str = "toman") -> str:
    """Convert monetary values to written Persian words with proper currency label (handles formatted inputs)."""
    currency = currency.lower()
    if currency not in _CURRENCY_LABELS:
        raise ValueError(f"Unknown currency '{currency}'")

    _persian_to_ascii = str.maketrans("۰۱۲۳۴۵۶۷۸۹٠١٢٣٤٥٦٧٨٩", "01234567890123456789")
    clean_amount = str(amount).replace(",", "").replace("،", "").replace(" ", "")
    normalized = clean_amount.translate(_persian_to_ascii)
    try:
        value = int(normalized)
    except ValueError:
        raise ValueError(f"Cannot convert '{amount}' to an integer amount.") from None

    words_part = number_to_words(value)
    label = _CURRENCY_LABELS[currency]
    return f"{words_part} {label}"


def add_tax_and_toll(amount: int | str, tax_rate: float = 0.10) -> int:
    """Calculate total amount including Value Added Tax (VAT). Default is 10%.

    Args:
        amount:   The price amount as int or string.
        tax_rate: Tax rate as float (e.g. 0.10 for 10%).

    Returns:
        The total price including tax as an integer.
    """
    _persian_to_ascii = str.maketrans("۰۱۲۳۴۵۶۷۸۹٠١٢٣٤٥٦٧٨٩", "01234567890123456789")
    clean_amount = str(amount).replace(",", "").replace("،", "").replace(" ", "")
    normalized = clean_amount.translate(_persian_to_ascii)
    try:
        val = int(normalized)
    except ValueError:
        raise ValueError(f"Invalid numeric input '{amount}' for tax calculations.") from None

    if val < 0:
        raise ValueError("Amount must be non-negative.")

    return int(val * (1 + tax_rate))


def calculate_installments(principal: int | str, annual_interest_rate: float, months: int) -> int:
    """Calculate the monthly installment amount for loan amortization.

    Args:
        principal:            The total loan amount.
        annual_interest_rate: Annual interest percentage (e.g. 18.0 or 23.0).
        months:               Number of payment months.

    Returns:
        The exact monthly installment amount as integer.
    """
    _persian_to_ascii = str.maketrans("۰۱۲۳۴۵۶۷۸۹٠١٢٣٤٥٦٧٨٩", "01234567890123456789")
    clean_amount = str(principal).replace(",", "").replace("،", "").replace(" ", "")
    normalized = clean_amount.translate(_persian_to_ascii)
    try:
        p = int(normalized)
    except ValueError:
        raise ValueError(f"Invalid loan principal '{principal}'.") from None

    if p <= 0 or months <= 0:
        raise ValueError("Loan principal and months must be greater than zero.")

    if annual_interest_rate == 0:
        return int(p / months)

    # Convert yearly percentage rate to a monthly decimal rate
    r = (annual_interest_rate / 100) / 12
    numerator = p * r * ((1 + r) ** months)
    denominator = ((1 + r) ** months) - 1
    return int(numerator / denominator)