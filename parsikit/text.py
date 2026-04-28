"""
parsikit.text
~~~~~~~~~~~~~
Persian text standardization and normalization utilities.

All transformations are performed using pre-built str.maketrans translation
tables for O(n) performance, avoiding repeated character-by-character checks.
"""

import re

# ---------------------------------------------------------------------------
# Translation table: Arabic → Persian character normalization
# ---------------------------------------------------------------------------
# Maps visually similar Arabic code-points to their canonical Persian forms.
_ARABIC_TO_PERSIAN_TABLE: dict[int, int] = str.maketrans(
    {
        # Arabic Yeh variants → Persian Yeh (U+06CC)
        "\u064A": "\u06CC",  # ي  → ی
        "\u0649": "\u06CC",  # ى  → ی  (Alef Maqsura)
        # Arabic Kaf → Persian Kaf (U+06A9)
        "\u0643": "\u06A9",  # ك  → ک
        # Arabic-Indic digits → Extended Arabic-Indic (used in Persian)
        "\u0660": "\u06F0",  # ٠ → ۰
        "\u0661": "\u06F1",  # ١ → ۱
        "\u0662": "\u06F2",  # ٢ → ۲
        "\u0663": "\u06F3",  # ٣ → ۳
        "\u0664": "\u06F4",  # ٤ → ۴
        "\u0665": "\u06F5",  # ٥ → ۵
        "\u0666": "\u06F6",  # ٦ → ۶
        "\u0667": "\u06F7",  # ٧ → ۷
        "\u0668": "\u06F8",  # ٨ → ۸
        "\u0669": "\u06F9",  # ٩ → ۹
        # Trailing Arabic Heh variants → Persian Heh (U+0647)
        "\u06D5": "\u0647",  # ە → ه  (Ae in Kurdish/Arabic)
        # Arabic comma / semicolon → Persian equivalents
        "\u060C": "\u060C",  # ، (already correct, kept for completeness)
        "\u061B": "\u061B",  # ؛ (already correct)
    }
)

# ---------------------------------------------------------------------------
# ZWNJ (Zero-Width Non-Joiner / نیم‌فاصله) correction patterns
# ---------------------------------------------------------------------------
# Common Persian prefixes and suffixes that must be joined to their host word
# with a ZWNJ instead of a plain space.
#
# Strategy: compile patterns once at module load; apply in standardize_persian.

_ZWNJ = "\u200C"  # Zero-Width Non-Joiner

# Prefixes that should attach via ZWNJ: می، نمی، بی، هم، غیر، پیش، هر
_PREFIX_PATTERNS: list[tuple[re.Pattern, str]] = [
    # "می " / "نمی " followed by a verb stem → replace space with ZWNJ
    (re.compile(r"\b(می|نمی)\s+(?=\S)"), r"\1" + _ZWNJ),
    # "بی " / "هم " / "غیر " / "پیش " / "هر " as prefix
    (re.compile(r"\b(بی|هم|غیر|پیش|هر)\s+(?=\S)"), r"\1" + _ZWNJ),
]

# Suffixes that should attach via ZWNJ: ها، های، هایی، ای، ام، ات، اش، ایم، اید، اند
_SUFFIX_PATTERNS: list[tuple[re.Pattern, str]] = [
    (
        re.compile(r"(?<=\S)\s+(ها|های|هایی|ای|ام|ات|اش|ایم|اید|اند)\b"),
        _ZWNJ + r"\1",
    ),
]

# Merge all correction patterns for a single-pass application
_ZWNJ_PATTERNS: list[tuple[re.Pattern, str]] = (
    _PREFIX_PATTERNS + _SUFFIX_PATTERNS
)


def standardize_persian(text: str) -> str:
    """Normalize Persian/Arabic text to canonical Persian form.

    Performs the following transformations in order:

    1. Replaces Arabic characters with their Persian equivalents using a
       pre-built ``str.translate`` table (O(n), no regex overhead).
    2. Corrects Zero-Width Non-Joiner (ZWNJ / نیم‌فاصله) placement for
       common Persian prefixes (می، نمی، بی، …) and suffixes (ها، های، …).
    3. Collapses multiple consecutive spaces into a single space and strips
       leading/trailing whitespace.

    Args:
        text: Raw input string that may contain Arabic characters or
              incorrect spacing around Persian affixes.

    Returns:
        A normalized Persian string.

    Examples:
        >>> standardize_persian("ي كتاب")
        'ی کتاب'
        >>> standardize_persian("می روم")
        'می‌روم'
        >>> standardize_persian("كتاب ها")
        'کتاب‌ها'
    """
    if not text:
        return text

    # Step 1: character-level normalization via translation table
    text = text.translate(_ARABIC_TO_PERSIAN_TABLE)

    # Step 2: ZWNJ corrections
    for pattern, replacement in _ZWNJ_PATTERNS:
        text = pattern.sub(replacement, text)

    # Step 3: collapse redundant whitespace
    text = re.sub(r" {2,}", " ", text).strip()

    return text
