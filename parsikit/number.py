"""
parsikit.number
~~~~~~~~~~~~~~~
Digit conversion utilities between Persian (Extended Arabic-Indic),
Arabic-Indic, and ASCII digit sets.

All conversions use ``str.translate`` with pre-built tables for maximum
throughput — a single O(n) pass over the string with no branching per char.
"""

# ---------------------------------------------------------------------------
# Translation tables (built once at import time)
# ---------------------------------------------------------------------------

# ASCII / Arabic-Indic → Persian (Extended Arabic-Indic, U+06F0–U+06F9)
_TO_PERSIAN_TABLE: dict[int, int] = str.maketrans(
    {
        # ASCII digits
        "0": "\u06F0", "1": "\u06F1", "2": "\u06F2",
        "3": "\u06F3", "4": "\u06F4", "5": "\u06F5",
        "6": "\u06F6", "7": "\u06F7", "8": "\u06F8",
        "9": "\u06F9",
        # Arabic-Indic digits (U+0660–U+0669)
        "\u0660": "\u06F0", "\u0661": "\u06F1", "\u0662": "\u06F2",
        "\u0663": "\u06F3", "\u0664": "\u06F4", "\u0665": "\u06F5",
        "\u0666": "\u06F6", "\u0667": "\u06F7", "\u0668": "\u06F8",
        "\u0669": "\u06F9",
    }
)

# Persian / Arabic-Indic → ASCII digits
_TO_ENGLISH_TABLE: dict[int, int] = str.maketrans(
    {
        # Persian digits (U+06F0–U+06F9)
        "\u06F0": "0", "\u06F1": "1", "\u06F2": "2",
        "\u06F3": "3", "\u06F4": "4", "\u06F5": "5",
        "\u06F6": "6", "\u06F7": "7", "\u06F8": "8",
        "\u06F9": "9",
        # Arabic-Indic digits (U+0660–U+0669)
        "\u0660": "0", "\u0661": "1", "\u0662": "2",
        "\u0663": "3", "\u0664": "4", "\u0665": "5",
        "\u0666": "6", "\u0667": "7", "\u0668": "8",
        "\u0669": "9",
    }
)


def english_to_persian(text: str) -> str:
    """Convert ASCII and Arabic-Indic digits in *text* to Persian digits.

    Non-digit characters are passed through unchanged.

    Args:
        text: Input string potentially containing ASCII (0-9) or
              Arabic-Indic (٠-٩) digits.

    Returns:
        String with all digit characters replaced by Persian equivalents.

    Examples:
        >>> english_to_persian("Order 123")
        'Order ۱۲۳'
        >>> english_to_persian("١٢٣")   # Arabic-Indic input
        '۱۲۳'
    """
    if not text:
        return text
    return text.translate(_TO_PERSIAN_TABLE)


def persian_to_english(text: str) -> str:
    """Convert Persian and Arabic-Indic digits in *text* to ASCII digits.

    Essential before storing numeric strings in a database or performing
    arithmetic operations on user-supplied Persian input.

    Args:
        text: Input string potentially containing Persian (۰-۹) or
              Arabic-Indic (٠-٩) digits.

    Returns:
        String with all Persian/Arabic digit characters replaced by ASCII
        equivalents.

    Examples:
        >>> persian_to_english("قیمت: ۱۲۳۴")
        'قیمت: 1234'
        >>> persian_to_english("٩٨٧")   # Arabic-Indic input
        '987'
    """
    if not text:
        return text
    return text.translate(_TO_ENGLISH_TABLE)
