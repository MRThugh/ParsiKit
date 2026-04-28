"""
parsikit.currency
~~~~~~~~~~~~~~~~~
Currency formatting and unit conversion utilities for Iranian Rial and Toman.

Design notes:
- ``format_currency`` intentionally returns a plain string with ASCII commas
  so the result is safe for both display and further string processing.
- Persian digit rendering is left to the caller (pipe through
  ``english_to_persian`` if needed).
"""

from __future__ import annotations

# Supported currency labels (display strings)
_CURRENCY_LABELS: dict[str, str] = {
    "toman": "تومان",
    "rial": "ریال",
}


def format_currency(
    amount: int | str,
    currency: str = "toman",
    *,
    persian_digits: bool = False,
) -> str:
    """Format a numeric amount as a human-readable currency string.

    Inserts thousands separators (commas) and appends the currency label.
    Optionally renders digits in Persian script.

    Args:
        amount:         The monetary amount as an ``int`` or a numeric string.
                        Arabic/Persian digit strings are accepted and
                        normalized automatically.
        currency:       Currency unit — ``'toman'`` (default) or ``'rial'``.
        persian_digits: When ``True``, the digit portion of the output is
                        rendered in Persian script (۱،۰۰۰،۰۰۰ تومان).

    Returns:
        Formatted string, e.g. ``"1,000,000 تومان"``.

    Raises:
        ValueError: If *amount* cannot be interpreted as an integer, or if
                    *currency* is not a recognized label.

    Examples:
        >>> format_currency(1000000)
        '1,000,000 تومان'
        >>> format_currency(1000000, "rial")
        '1,000,000 ریال'
        >>> format_currency("۱۵۰۰۰۰", persian_digits=True)
        '۱۵۰،۰۰۰ تومان'
    """
    currency = currency.lower()
    if currency not in _CURRENCY_LABELS:
        raise ValueError(
            f"Unknown currency '{currency}'. "
            f"Supported values: {list(_CURRENCY_LABELS)}"
        )

    # Normalize Persian/Arabic digits to ASCII before int conversion
    normalized = str(amount)
    _persian_to_ascii = str.maketrans(
        "۰۱۲۳۴۵۶۷۸۹٠١٢٣٤٥٦٧٨٩",
        "01234567890123456789",
    )
    normalized = normalized.translate(_persian_to_ascii)

    try:
        value = int(normalized)
    except ValueError:
        raise ValueError(
            f"Cannot convert '{amount}' to an integer amount."
        ) from None

    label = _CURRENCY_LABELS[currency]

    if persian_digits:
        # Format with Persian thousands separator (،) and Persian digits
        formatted = _format_with_persian_digits(value)
        return f"{formatted} {label}"

    return f"{value:,} {label}"


def rial_to_toman(amount: int) -> int:
    """Convert an amount in Iranian Rial to Toman.

    The Toman is an informal unit equal to 10 Rials and is the de-facto
    unit used in everyday Iranian commerce.

    Args:
        amount: Amount in Rial (must be a non-negative integer).

    Returns:
        Equivalent amount in Toman (integer division by 10).

    Raises:
        ValueError: If *amount* is negative.

    Examples:
        >>> rial_to_toman(10000)
        1000
        >>> rial_to_toman(15)   # fractional Toman → truncated
        1
    """
    if amount < 0:
        raise ValueError("Amount must be non-negative.")
    return amount // 10


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _format_with_persian_digits(value: int) -> str:
    """Return *value* formatted with commas replaced by '،' and ASCII digits
    replaced by Persian digits (U+06F0–U+06F9)."""
    _to_persian = str.maketrans("0123456789,", "۰۱۲۳۴۵۶۷۸۹،")
    return f"{value:,}".translate(_to_persian)
