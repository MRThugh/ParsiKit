"""
parsikit.text
~~~~~~~~~~~~~
Text standardization, normalization, and keyboard layout correction.
"""

import re

# Table for converting Arabic characters to Persian equivalents
_ARABIC_TO_PERSIAN_TABLE: dict[int, int] = str.maketrans(
    {
        "\u064A": "\u06CC",  # ي  → ی
        "\u0649": "\u06CC",  # ى  → ی
        "\u0643": "\u06A9",  # ك  → ک
        "\u0660": "\u06F0", "\u0661": "\u06F1", "\u0662": "\u06F2", "\u0663": "\u06F3",
        "\u0664": "\u06F4", "\u0665": "\u06F5", "\u0666": "\u06F6", "\u0667": "\u06F7",
        "\u0668": "\u06F8", "\u0669": "\u06F9",
        "\u06D5": "\u0647",  # ە → ه
        "\u0629": "\u0647",  # ة → ه
        "\u06C0": "\u0647\u0654",  # ۀ → هٔ
    }
)

# Standard QWERTY keys mapped to standard Persian keyboard (with shift & punctuation fixes)
_QWERTY_TO_PERSIAN_MAP = {
    'q': 'ض', 'w': 'ص', 'e': 'ث', 'r': 'ق', 't': 'ف', 'y': 'غ', 'u': 'ع', 'i': 'ه', 'o': 'خ', 'p': 'ح', '[': 'ج', ']': 'چ',
    'a': 'ش', 's': 'س', 'd': 'ی', 'f': 'ب', 'g': 'ل', 'h': 'ا', 'j': 'ت', 'k': 'ن', 'l': 'م', ';': 'ک', "'": 'گ',
    'z': 'ظ', 'x': 'ط', 'c': 'ز', 'v': 'ر', 'b': 'ذ', 'n': 'د', 'm': 'پ', ',': 'و',
    'Q': 'ض', 'W': 'ص', 'E': 'ث', 'R': 'ق', 'T': 'ف', 'Y': 'غ', 'U': 'ع', 'I': 'ه', 'O': 'خ', 'P': 'ح', '{': 'ج', '}': 'چ',
    'A': 'ش', 'S': 'س', 'D': 'ی', 'F': 'ب', 'G': 'ل', 'H': 'آ', 'J': 'ت', 'K': 'ن', 'L': 'م', ':': 'ک', '"': 'گ',
    'Z': 'ظ', 'X': 'ط', 'C': 'ز', 'V': 'ر', 'B': 'ذ', 'N': 'د', 'M': 'پ', '<': 'و',
    '\\': 'ژ', '|': 'ژ',
    '?': '؟',
}
_KEYBOARD_TABLE = str.maketrans(_QWERTY_TO_PERSIAN_MAP)

_ZWNJ = "\u200C"

# Robust prefixes
_PREFIX_PATTERNS = [
    (re.compile(r"\b(می|نمی)\s+(?=\S)"), r"\1" + _ZWNJ),
    (re.compile(r"\b(بی)\s+(?=\S)"), r"\1" + _ZWNJ),
]

# Suffixes including comparative adjectives "تر" and "ترین"
_SUFFIX_PATTERNS = [
    (
        re.compile(r"(?<=\S)\s+(ها|های|هایی|تر|ترین|ای|ام|ات|اش|ایم|اید|اند)\b"),
        _ZWNJ + r"\1",
    ),
]

_ZWNJ_PATTERNS = _PREFIX_PATTERNS + _SUFFIX_PATTERNS


def strip_diacritics(text: str) -> str:
    """Remove Arabic/Persian diacritics (Fatha, Kasra, Damma, Tanween, Tashdeed, Sukuun)."""
    if not text:
        return text
    diacritics_pattern = re.compile(r"[\u064B-\u065F\u0670]")
    return diacritics_pattern.sub("", text)


def is_persian(text: str) -> bool:
    """Check if the text contains at least one Persian/Arabic script character (including reshaped forms)."""
    if not text:
        return False
    # Unicode ranges: standard Arabic/Persian + Supplements + Presentation Forms-A & Forms-B
    return bool(re.search(r"[\u0600-\u06FF\u0750-\u077F\uFB50-\uFDFF\uFE70-\uFEFF]", text))


def correct_keyboard_layout(text: str) -> str:
    """Correct English layout typed text into Persian layout (e.g. 'sghl' -> 'سلام')."""
    if not text:
        return text
    return text.translate(_KEYBOARD_TABLE)


def standardize_persian(text: str, *, strip_diacritics_opt: bool = False) -> str:
    """Normalize and standardize Persian text layout, character codes, and spaces."""
    if not text:
        return text

    if strip_diacritics_opt:
        text = strip_diacritics(text)

    # Convert characters
    text = text.translate(_ARABIC_TO_PERSIAN_TABLE)

    # Adjust ZWNJs
    for pattern, replacement in _ZWNJ_PATTERNS:
        text = pattern.sub(replacement, text)

    # Collapse redundant spaces
    text = re.sub(r" {2,}", " ", text).strip()

    return text


def persian_sort_key(s: str) -> list[int]:
    """Generate a sorting key for Persian strings to allow proper alphabetical ordering."""
    if not isinstance(s, str):
        return [0]
    
    # Normalize characters inside key generator to handle Arabic ی and ک
    _norm_map = str.maketrans({
        "ي": "ی", "ى": "ی", "ك": "ک",
        "ة": "ه", "ۀ": "ه",
    })
    s = s.translate(_norm_map).lower()
    
    # Standard Persian Alphabetical Order
    persian_alphabet = "آابپتثجچحخدذرزژسشصضطظعغفقکگلمنوهی"
    weights = {char: idx for idx, char in enumerate(persian_alphabet)}
    
    key = []
    for char in s:
        if char == ' ':
            key.append(-100)
        elif char == '\u200C': # ZWNJ
            key.append(-99)
        elif char.isdigit():
            # Support both English and Persian digits
            digit_map = str.maketrans("۰۱۲۳۴۵۶۷۸۹٠١٢٣٤٥٦٧٨٩", "01234567890123456789")
            try:
                digit_val = int(char.translate(digit_map))
                key.append(-50 + digit_val)
            except ValueError:
                key.append(ord(char))
        elif char in weights:
            key.append(1000 + weights[char])
        else:
            # English letters and other symbols
            key.append(ord(char))
            
    return key


def persian_sorted(iterable, *, reverse: bool = False):
    """Sort an iterable alphabetically using correct Persian collation weights."""
    return sorted(iterable, key=persian_sort_key, reverse=reverse)


def beautify_persian_spacing(text: str) -> str:
    """Optimize and beautify spaces around Persian punctuation and symbols.
    
    Creates a much more comfortable typing and reading feel for Persian users by:
    - Automatically converting English commas and semicolons to Persian equivalents (، , ؛)
      when they are surrounded by Persian script.
    - Removing spaces before punctuation marks (., ،, ؛, ؟, !, :)
    - Ensuring exactly one space exists after punctuation.
    - Removing spaces inside parentheses, brackets, and braces: ( text ) -> (text).
    """
    if not text:
        return text
        
    # 1. Convert English commas and semicolons when typed amidst Persian text (with or without spaces)
    text = re.sub(r"([\u0600-\u06FF])\s*,\s*(?=[\u0600-\u06FF])", r"\1، ", text)
    text = re.sub(r"([\u0600-\u06FF])\s*;\s*(?=[\u0600-\u06FF])", r"\1؛ ", text)

    # 2. Remove spaces before standard Persian and English punctuation
    text = re.sub(r"\s+([.،؛؟?!:])", r"\1", text)
    
    # 3. Ensure exactly one space after punctuation
    text = re.sub(r"([.،؛؟?!:])(?=[^\s.،؛؟?!:])", r"\1 ", text)

    # 4. Collapse spaces inside parenthetical enclosures
    text = re.sub(r"\(\s+", "(", text)
    text = re.sub(r"\s+\)", ")", text)
    text = re.sub(r"\[\s+", "[", text)
    text = re.sub(r"\s+\]", "]", text)
    text = re.sub(r"\{\s+", "{", text)
    text = re.sub(r"\s+\}", "}", text)

    # Ensure outside spacing around parentheses and brackets
    text = re.sub(r"(\S)\(", r"\1 (", text)
    text = re.sub(r"\)(\S)", r") \1", text)
    text = re.sub(r"(\S)\[", r"\1 [", text)
    text = re.sub(r"\](\S)", r"] \1", text)

    # Standardize redundant spaces
    text = re.sub(r" {2,}", " ", text).strip()
    return text