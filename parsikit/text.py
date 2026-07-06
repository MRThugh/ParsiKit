"""
parsikit.text
~~~~~~~~~~~~~
Text standardization, normalization, and keyboard layout correction.
"""

from __future__ import annotations
from typing import Iterable, TypeVar
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

_T = TypeVar("_T")


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
    
    _norm_map = str.maketrans({
        "ي": "ی", "ى": "ی", "ك": "ک",
        "ة": "ه", "ۀ": "ه",
    })
    s = s.translate(_norm_map).lower()
    
    persian_alphabet = "آابپتثجچحخدذرزژسشصضطظعغفقکگلمنوهی"
    weights = {char: idx for idx, char in enumerate(persian_alphabet)}
    
    key = []
    for char in s:
        if char == ' ':
            key.append(-100)
        elif char == '\u200C': # ZWNJ
            key.append(-99)
        elif char.isdigit():
            digit_map = str.maketrans("۰۱۲۳۴۵۶۷۸۹٠١٢٣٤٥٦٧٨٩", "01234567890123456789")
            try:
                digit_val = int(char.translate(digit_map))
                key.append(-50 + digit_val)
            except ValueError:
                key.append(ord(char))
        elif char in weights:
            key.append(1000 + weights[char])
        else:
            key.append(ord(char))
            
    return key


def persian_sorted(iterable: Iterable[_T], *, reverse: bool = False) -> list[_T]:
    """Sort an iterable alphabetically using correct Persian collation weights."""
    return sorted(iterable, key=persian_sort_key, reverse=reverse)  # type: ignore


def beautify_persian_spacing(text: str) -> str:
    """Optimize and beautify spaces around Persian punctuation and symbols."""
    if not text:
        return text
        
    text = re.sub(r"([\u0600-\u06FF])\s*,\s*(?=[\u0600-\u06FF])", r"\1، ", text)
    text = re.sub(r"([\u0600-\u06FF])\s*;\s*(?=[\u0600-\u06FF])", r"\1؛ ", text)

    text = re.sub(r"\s+([.،؛؟?!:])", r"\1", text)
    text = re.sub(r"([.،؛؟?!:])(?=[^\s.،؛؟?!:])", r"\1 ", text)

    text = re.sub(r"\s+\)", ")", text)
    text = re.sub(r"\[\s+", "[", text)
    text = re.sub(r"\s+\]", "]", text)
    text = re.sub(r"\{\s+", "{", text)
    text = re.sub(r"\s+\}", "}", text)

    text = re.sub(r"(\S)\(", r"\1 (", text)
    text = re.sub(r"\)(\S)", r") \1", text)
    text = re.sub(r"(\S)\[", r"\1 [", text)
    text = re.sub(r"\](\S)", r"] \1", text)

    text = re.sub(r" {2,}", " ", text).strip()
    return text


def extract_mobiles(text: str) -> list[str]:
    """Extract and normalize all unique Iranian mobile numbers found inside a raw text block."""
    if not text:
        return []
    
    _TO_ENGLISH_LOCAL = str.maketrans("۰۱۲۳۴۵۶۷۸۹٠١٢٣٤٥٦٧٨٩", "01234567890123456789")
    eng_text = text.translate(_TO_ENGLISH_LOCAL)
    
    pattern = re.compile(r"\b(?:\+98|0098|98|0)?9\d{9}\b")
    matches = pattern.findall(eng_text)
    
    from parsikit.validators import normalize_mobile, is_valid_mobile
    normalized_list = []
    for match in matches:
        if is_valid_mobile(match):
            normalized_list.append(normalize_mobile(match, prefix="0"))
            
    seen = set()
    result = []
    for num in normalized_list:
        if num not in seen:
            seen.add(num)
            result.append(num)
    return result


def extract_national_codes(text: str) -> list[str]:
    """Extract and validate all Iranian national codes (کد ملی) found inside a raw text block."""
    if not text:
        return []
    
    _TO_ENGLISH_LOCAL = str.maketrans("۰۱۲۳۴۵۶۷۸۹٠١٢٣٤٥٦٧٨٩", "01234567890123456789")
    eng_text = text.translate(_TO_ENGLISH_LOCAL)
    
    pattern = re.compile(r"\b\d{10}\b|\b\d{3}-\d{6}-\d\b")
    matches = pattern.findall(eng_text)
    
    from parsikit.validators import is_valid_national_code
    valid_codes = []
    for match in matches:
        clean_code = match.replace("-", "")
        if is_valid_national_code(clean_code):
            valid_codes.append(clean_code)
            
    seen = set()
    result = []
    for code in valid_codes:
        if code not in seen:
            seen.add(code)
            result.append(code)
    return result


def words_to_number(text: str) -> int:
    """Convert Persian textual numbers (e.g. 'سی و دو هزار و پانصد') back into an integer.
    
    Supports exceptionally large values up to Septillions.
    """
    if not text:
        return 0

    clean_text = text.replace("،", "").replace(",", "").strip()
    
    ones = {
        "صفر": 0, "یک": 1, "دو": 2, "سه": 3, "چهار": 4, "پنج": 5, "شش": 6, "هفت": 7, "هشت": 8, "نه": 9,
    }
    teens = {
        "ده": 10, "یازده": 11, "دوازده": 12, "سیزده": 13, "چهارده": 14, "پانزده": 15, "شانزده": 16,
        "هفده": 17, "هجده": 18, "نوزده": 19
    }
    tens = {
        "بیست": 20, "سی": 30, "چهل": 40, "پنجاه": 50, "شصت": 60, "هفتاد": 70, "هشتاد": 80, "نود": 90
    }
    hundreds = {
        "یکصد": 100, "صد": 100, "دویست": 200, "سیصد": 300, "چهارصد": 400, "پانصد": 500,
        "ششصد": 600, "هفتصد": 700, "هشتصد": 800, "نهصد": 900
    }
    scales = {
        "هزار": 1000,
        "میلیون": 1000000,
        "میلیارد": 1000000000,
        "تریلیون": 1000000000000,
        "کوآدریلیون": 1000000000000000,
        "کوئینتیلیون": 1000000000000000000,
        "سکستیلیون": 1000000000000000000000,
        "سپتیلیون": 1000000000000000000000000,
    }

    raw_tokens = [t.strip() for t in clean_text.split(" ") if t.strip()]
    tokens = []
    for token in raw_tokens:
        if token == "و":
            continue
        tokens.append(token)

    total = 0
    current_group = 0
    is_neg = False

    if tokens and tokens[0] == "منفی":
        is_neg = True
        tokens.pop(0)

    for token in tokens:
        if token in ones:
            current_group += ones[token]
        elif token in teens:
            current_group += teens[token]
        elif token in tens:
            current_group += tens[token]
        elif token in hundreds:
            current_group += hundreds[token]
        elif token in scales:
            scale = scales[token]
            if current_group == 0:
                current_group = 1
            total += current_group * scale
            current_group = 0
        else:
            try:
                from parsikit.number import persian_to_english
                num = int(persian_to_english(token))
                current_group += num
            except ValueError:
                continue

    total += current_group
    return -total if is_neg else total