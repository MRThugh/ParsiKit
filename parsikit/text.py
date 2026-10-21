"""
parsikit.text
~~~~~~~~~~~~~
Text standardization, normalization, and keyboard layout correction.
"""

from __future__ import annotations
from typing import Iterable, TypeVar, Literal
import re
import unicodedata

# Table for converting Arabic characters to Persian equivalents in Persian text context
_ARABIC_TO_PERSIAN_TABLE: dict[int, int] = str.maketrans(
    {
        "\u064A": "\u06CC",  # ي  → ی
        "\u0649": "\u06CC",  # ى  → ی
        "\u0643": "\u06A9",  # ك  → ک
        "\u0660": "\u06F0", "\u0661": "\u06F1", "\u0662": "\u06F2", "\u0663": "\u06F3",
        "\u0664": "\u06F4", "\u0665": "\u06F5", "\u0666": "\u06F6", "\u0667": "\u06F7",
        "\u0668": "\u06F8", "\u0669": "\u06F9",
        "\u0629": "\u0647",  # ة → ه (Arabic Ta Marbuta in Persian loanword context)
        "\u06C0": "\u0647\u0654",  # ۀ → هٔ
    }
)

# Safe mapping for multilingual preservation: keeps Arabic/Kurdish characters intact
_MULTILINGUAL_SAFE_TABLE: dict[int, int] = str.maketrans({})

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

# Precompiled prefix and suffix patterns for ZWNJ adjustment
_PREFIX_PATTERNS = [
    (re.compile(r"\b(می|نمی)[\s\u200C]+(?=\S)"), r"\1" + _ZWNJ),
    (re.compile(r"\b(بی)[\s\u200C]+(?=\S)"), r"\1" + _ZWNJ),
]

_SUFFIX_PATTERNS = [
    (
        re.compile(r"(?<=\S)[\s\u200C]+(ها|های|هایی|تر|ترین|ای|ام|ات|اش|ایم|اید|اند)\b"),
        _ZWNJ + r"\1",
    ),
]

_ZWNJ_PATTERNS = _PREFIX_PATTERNS + _SUFFIX_PATTERNS

# Precompiled ZWNJ cleanup regular expressions
_SPACE_ZWNJ_SPACE_PATTERN = re.compile(r"[\t ]+\u200C+[\t ]+")
_SPACE_ZWNJ_PATTERN = re.compile(r"[\t ]+\u200C")
_ZWNJ_SPACE_PATTERN = re.compile(r"\u200C[\t ]+")
_PUNCT_ZWNJ_PATTERN1 = re.compile(r"\u200C+([.,،؛؟?!:()\[\]{}«»])")
_PUNCT_ZWNJ_PATTERN2 = re.compile(r"([.,،؛؟?!:()\[\]{}«»])\u200C+")
_DUPLICATE_ZWNJ_PATTERN = re.compile(r"\u200C{2,}")
_STRIP_ZWNJ_PATTERN = re.compile(r"^\u200C+|\u200C+$")
_MULTI_SPACE_PATTERN = re.compile(r" {2,}")
_DIACRITICS_PATTERN = re.compile(r"[\u064B-\u065F\u0670]")
_PERSIAN_CHAR_PATTERN = re.compile(r"[\u0600-\u06FF\u0750-\u077F\uFB50-\uFDFF\uFE70-\uFEFF]")

# Precompiled punctuation spacing patterns
_PERSIAN_COMMA_RE = re.compile(r"([\u0600-\u06FF])\s*,\s*(?=[\u0600-\u06FF])")
_PERSIAN_SEMICOLON_RE = re.compile(r"([\u0600-\u06FF])\s*;\s*(?=[\u0600-\u06FF])")
_SPACE_BEFORE_PUNCT_RE = re.compile(r"\s+([.،؛؟?!:])")
_PERSIAN_PUNCT_SPACE_RE = re.compile(r"([،؛؟])(?=[^\s،؛؟])")
_EXCLAMATION_SPACE_RE = re.compile(r"(!)(?=[^\s!])")
_QUESTION_SPACE_RE = re.compile(r"(\?)(?=[^\s?])")
_ALL_DIGITS_CLASS = r"0-9\u06F0-\u06F9\u0660-\u0669"
_COLON_SPACE_RE = re.compile(rf"(?<!\bhttp)(?<!\bhttps)(?<!\bftp)(?<![{_ALL_DIGITS_CLASS}]):(?![/{_ALL_DIGITS_CLASS}\s])")
_PERIOD_SPACE_RE = re.compile(rf"(?<=[\u0600-\u06EF\u06FA-\u06FF])\.(?=[^\s.{_ALL_DIGITS_CLASS}])")

_OPEN_BRACKET_SPACE_RE1 = re.compile(r"([^\s«(\[{])\(")
_OPEN_BRACKET_SPACE_RE2 = re.compile(r"\)([^\s.,;!?؟،؛:)\x5d}»])")
_OPEN_SQBRACKET_SPACE_RE1 = re.compile(r"([^\s«(\[{])\[")
_OPEN_SQBRACKET_SPACE_RE2 = re.compile(r"\]([^\s.,;!?؟،؛:)\x5d}»])")
_OPEN_PAREN_TRIM_RE = re.compile(r"\(\s+")
_CLOSE_PAREN_SPACE_RE = re.compile(r"\s+\)")
_OPEN_SQBRACKET_TRIM_RE = re.compile(r"\[\s+")
_CLOSE_SQBRACKET_TRIM_RE = re.compile(r"\s+\]")
_OPEN_BRACE_TRIM_RE = re.compile(r"\{\s+")
_CLOSE_BRACE_TRIM_RE = re.compile(r"\s+\}")
_OPEN_GUILLEMET_TRIM_RE = re.compile(r"«\s+")
_CLOSE_GUILLEMET_TRIM_RE = re.compile(r"\s+»")
_OPEN_GUILLEMET_SPACE_RE = re.compile(r"([^\s«(\[{])«")
_CLOSE_GUILLEMET_SPACE_RE = re.compile(r"»([^\s.,;!?؟،؛:)\x5d}»])")

# Technical token protection patterns
_URL_PATTERN = re.compile(r"(?:https?|ftp)://[^\s<>\x22\x27\x60]+")
_EMAIL_PATTERN = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")
_KEY_VAL_PATTERN = re.compile(r"\b[A-Za-z_][A-Za-z0-9_]*=[A-Za-z0-9_./+-]+")
_SEMVER_PATTERN = re.compile(r"\b(?:v\d+(?:\.\d+)+(?:-[A-Za-z0-9.]+)?|\d+(?:\.\d+){2,}(?:-[A-Za-z0-9.]+)?)\b")
_TECH_ID_PATTERN = re.compile(r"\b[A-Za-z0-9]+(?:-[A-Za-z0-9]+)+\b")


def _id_to_letters(n: int) -> str:
    res: list[str] = []
    while True:
        res.append(chr(ord("A") + (n % 26)))
        n //= 26
        if n == 0:
            break
    return "".join(reversed(res))


def _protect_tokens(text: str) -> tuple[str, dict[str, str]]:
    """Protect URLs, emails, and technical identifiers from spacing and digit transformations."""
    if not text:
        return text, {}

    token_map: dict[str, str] = {}
    counter = 0

    def get_ph(orig: str) -> str:
        nonlocal counter
        ph = f"\uE000PRSKT_{_id_to_letters(counter)}\uE001"
        counter += 1
        token_map[ph] = orig
        return ph

    # 1. URLs: preserve full query strings, fragments, paths, ports, percent-encoding
    def url_repl(m: re.Match[str]) -> str:
        raw = m.group(0)
        trailing = ""
        while raw and raw[-1] in ".,;!?؟،؛:":
            trailing = raw[-1] + trailing
            raw = raw[:-1]
        if raw.endswith(")") and raw.count(")") > raw.count("("):
            trailing = ")" + trailing
            raw = raw[:-1]
        elif raw.endswith("]") and raw.count("]") > raw.count("["):
            trailing = "]" + trailing
            raw = raw[:-1]
        elif raw.endswith("}") and raw.count("}") > raw.count("{"):
            trailing = "}" + trailing
            raw = raw[:-1]
        return get_ph(raw) + trailing

    text = _URL_PATTERN.sub(url_repl, text)

    # 2. Email addresses
    text = _EMAIL_PATTERN.sub(lambda m: get_ph(m.group(0)), text)

    # 3. Key-value technical tokens (e.g. version=v2.0.1)
    text = _KEY_VAL_PATTERN.sub(lambda m: get_ph(m.group(0)), text)

    # 4. Technical hyphenated IDs (e.g. ID-2026-0042)
    def id_repl(m: re.Match[str]) -> str:
        raw = m.group(0)
        if any(c.isdigit() for c in raw) and any(c.isalpha() for c in raw):
            return get_ph(raw)
        return raw

    text = _TECH_ID_PATTERN.sub(id_repl, text)

    # 5. Semantic versions and multi-dot technical numbers (e.g. v2.0.1, 3.13.3)
    text = _SEMVER_PATTERN.sub(lambda m: get_ph(m.group(0)), text)

    return text, token_map


def _restore_tokens(text: str, token_map: dict[str, str]) -> str:
    """Restore protected tokens to their pristine original form."""
    if not text or not token_map:
        return text
    for ph, orig in token_map.items():
        text = text.replace(ph, orig)
    return text

# Collation weights for Persian alphabetical sorting
_SORT_NORM_MAP = str.maketrans({
    "ي": "ی", "ى": "ی", "ك": "ک",
    "ة": "ه", "ۀ": "ه",
    "أ": "ا", "إ": "ا", "ٱ": "ا",
    "ؤ": "و", "ئ": "ی",
})
_PERSIAN_ALPHABET = "آابپتثجچحخدذرزژسشصضطظعغفقکگلمنوهی"
_PERSIAN_WEIGHTS: dict[str, int] = {char: 1000 + idx for idx, char in enumerate(_PERSIAN_ALPHABET)}
_DIGIT_CONV = str.maketrans("۰۱۲۳۴۵۶۷۸۹٠١٢٣٤٥٦٧٨٩", "01234567890123456789")

# Text extraction & cleaning patterns
_TO_ENGLISH_LOCAL = str.maketrans("۰۱۲۳۴۵۶۷۸۹٠١٢٣٤٥٦٧٨٩", "01234567890123456789")
_MOBILE_PATTERN = re.compile(r"\b(?:\+98|0098|98|0)?[\s-]?(?:9\d{9}|9(?:[\s-]?\d){9})\b")
_NATIONAL_CODE_PATTERN = re.compile(r"\b\d{10}\b|\b\d{3}[-\s]\d{6}[-\s]\d\b")
_CONTROL_CHARS_PATTERN = re.compile(r"[\u200B\uFEFF\u200E\u200F\u202A-\u202E]")
_REDUNDANT_NEWLINES_PATTERN = re.compile(r"\n{3,}")
_UNICODE_SPACES_PATTERN = re.compile(r"[\t\xa0\u2007\u2008\u2009\u200A\u202F]+")
_SLUG_TOKEN_PATTERN = re.compile(r"[a-z0-9\u0600-\u06FF\uFB50-\uFDFF\uFE70-\uFEFF]+")

# Persian written numbers mapping
_ONES = {
    "صفر": 0, "یک": 1, "دو": 2, "سه": 3, "چهار": 4, "پنج": 5, "شش": 6, "هفت": 7, "هشت": 8, "نه": 9,
}
_TEENS = {
    "ده": 10, "یازده": 11, "دوازده": 12, "سیزده": 13, "چهارده": 14, "پانزده": 15, "شانزده": 16,
    "هفده": 17, "هجده": 18, "نوزده": 19
}
_TENS = {
    "بیست": 20, "سی": 30, "چهل": 40, "پنجاه": 50, "شصت": 60, "هفتاد": 70, "هشتاد": 80, "نود": 90
}
_HUNDREDS = {
    "یکصد": 100, "صد": 100, "دویست": 200, "سیصد": 300, "چهارصد": 400, "پانصد": 500,
    "ششصد": 600, "هفتصد": 700, "هشتصد": 800, "نهصد": 900
}
_SCALES = {
    "هزار": 1000,
    "میلیون": 1000000,
    "میلیارد": 1000000000,
    "تریلیون": 1000000000000,
    "کوآدریلیون": 1000000000000000,
    "کوئینتیلیون": 1000000000000000000,
    "سکستیلیون": 1000000000000000000000,
    "سپتیلیون": 1000000000000000000000000,
}

# Character mapping dictionary for Persian-to-Finglish Romanization
_CHAR_TRANS_TABLE = {
    'آ': 'a', 'ا': 'a', 'ب': 'b', 'پ': 'p', 'ت': 't', 'ث': 's', 'ج': 'j', 'چ': 'ch', 'ح': 'h', 'خ': 'kh',
    'د': 'd', 'ذ': 'z', 'ر': 'r', 'ز': 'z', 'ژ': 'zh', 'س': 's', 'ش': 'sh', 'ص': 's', 'ض': 'z', 'ط': 't',
    'ظ': 'z', 'ع': 'a', 'غ': 'gh', 'ف': 'f', 'ق': 'gh', 'ک': 'k', 'گ': 'g', 'ل': 'l', 'م': 'm', 'ن': 'n',
    'و': 'v', 'ه': 'h', 'ی': 'y', 'ئ': 'y', 'ء': 'a', 'ۀ': 'h', 'ة': 'h',
    'أ': 'a', 'إ': 'e', 'ٱ': 'a'
}

# Sub-dictionary for popular Persian words and prepositions to keep slugs clean and meaningful
_COMMON_WORDS_PINGLISH = {
    "سلام": "salam",
    "دنیا": "donya",
    "خوب": "khoob",
    "بد": "bad",
    "امروز": "emrooz",
    "تهران": "tehran",
    "ایران": "iran",
    "کتاب": "ketab",
    "آسمان": "aseman",
    "باد": "bad",
    "باران": "baran",
    "آب": "ab",
    "نان": "nan",
    "خانه": "khaneh",
    "عشق": "eshgh",
    "دوست": "doost",
    "پدر": "pedar",
    "مادر": "madar",
    "برادر": "baradar",
    "خواهر": "khahar",
    "پسر": "pesar",
    "دختر": "dokhtar",
    "مرد": "mard",
    "زن": "zan",
    "بچه": "bacheh",
    "شب": "shab",
    "روز": "rooz",
    "صبح": "sobh",
    "عصر": "asr",
    "خواب": "khwab",
    "راه": "rah",
    "کار": "kar",
    "پول": "pool",
    "خرید": "kharid",
    "فروش": "foroosh",
    "فروشگاه": "forooshgah",
    "راهنما": "rahnama",
    "راهنمای": "rahnamaye",
    "مدرسه": "madreseh",
    "دانشگاه": "daneshgah",
    "استاد": "ostad",
    "کلاس": "kelas",
    "درس": "dars",
    "آموزش": "amoozesh",
    "وردپرس": "wordpress",
    "پایتون": "python",
    "برنامه": "barnameh",
    "نویسی": "nevisi",
    "وب": "web",
    "سایت": "site",
    "دانلود": "download",
    "مقاله": "maghaleh",
    "محصول": "mahsool",
    "نسخه": "neskheh",
    "در": "dar",
    "از": "az",
    "با": "ba",
    "به": "be",
    "تا": "ta",
    "برای": "baraye",
    "این": "in",
    "آن": "an",
}

_T = TypeVar("_T")


def strip_diacritics(text: str) -> str:
    """Remove Arabic/Persian diacritics (Fatha, Kasra, Damma, Tanween, Tashdeed, Sukuun)."""
    if not text:
        return text
    return _DIACRITICS_PATTERN.sub("", text)


def is_persian(text: str) -> bool:
    """Check if the text contains at least one Persian/Arabic script character (including reshaped forms)."""
    if not text:
        return False
    return bool(_PERSIAN_CHAR_PATTERN.search(text))


def correct_keyboard_layout(text: str) -> str:
    """Correct English layout typed text into Persian layout (e.g. 'sghl' -> 'سلام')."""
    if not text:
        return text
    return text.translate(_KEYBOARD_TABLE)


def standardize_persian(
    text: str,
    *,
    strip_diacritics_opt: bool = False,
    preserve_arabic: bool = False,
) -> str:
    """Normalize and standardize Persian text layout, character codes, and spaces.
    
    Applies:
    1. Unicode canonical NFC normalization.
    2. Optional diacritic stripping if requested.
    3. Arabic-to-Persian letter normalization (ي/ك/ة to ی/ک/ه) in Persian context.
       If preserve_arabic=True, Arabic-specific characters (ة, ي) are preserved.
       Kurdish characters such as Kurdish Ae (ە / U+06D5) are always preserved.
    4. ZWNJ insertion for prefixes (می‌/نمی‌/بی‌) and suffixes (‌ها/‌ترین/...).
    5. Clean-up of space-adjacent ZWNJ without joining independent words.
    6. Stripping of redundant ZWNJ characters adjacent to punctuation marks.
    7. Deduplication of adjacent ZWNJs and removal of leading/trailing ZWNJs.
    8. Redundant multi-space collapsing and edge trimming (preserving newlines).
    """
    if not text:
        return text

    # 1. Unicode canonical normalization (NFC)
    text = unicodedata.normalize("NFC", text)

    # 2. Optional diacritics removal
    if strip_diacritics_opt:
        text = strip_diacritics(text)

    # 3. Convert Arabic character variants to Persian
    if not preserve_arabic:
        text = text.translate(_ARABIC_TO_PERSIAN_TABLE)
    else:
        text = text.translate(_MULTILINGUAL_SAFE_TABLE)

    # 4. Adjust ZWNJs around prefixes and suffixes
    for pattern, replacement in _ZWNJ_PATTERNS:
        text = pattern.sub(replacement, text)

    # 5. Clean up spaces around ZWNJ:
    # Multiple spaces on both sides of ZWNJ between independent words -> single regular space
    text = _SPACE_ZWNJ_SPACE_PATTERN.sub(" ", text)
    # Single-sided space adjacent to ZWNJ -> ZWNJ (meaningful Persian half-space)
    text = _SPACE_ZWNJ_PATTERN.sub(_ZWNJ, text)
    text = _ZWNJ_SPACE_PATTERN.sub(_ZWNJ, text)

    # 6. Remove redundant ZWNJ adjacent to punctuation
    text = _PUNCT_ZWNJ_PATTERN1.sub(r"\1", text)
    text = _PUNCT_ZWNJ_PATTERN2.sub(r"\1", text)

    # 7. Collapse duplicate ZWNJs into single ZWNJ
    text = _DUPLICATE_ZWNJ_PATTERN.sub(_ZWNJ, text)

    # 8. Strip leading/trailing ZWNJs per line and collapse spaces, preserving line breaks
    lines = []
    for line in text.split("\n"):
        line = _STRIP_ZWNJ_PATTERN.sub("", line.strip())
        line = _MULTI_SPACE_PATTERN.sub(" ", line)
        lines.append(line)

    return "\n".join(lines).strip()


def persian_sort_key(s: str) -> tuple[int, ...]:
    """Generate a sorting key tuple for Persian strings to allow proper alphabetical ordering."""
    if not isinstance(s, str):
        return (0,)
    
    s = s.translate(_SORT_NORM_MAP).lower()
    
    key: list[int] = []
    for char in s:
        if char == ' ':
            key.append(-100)
        elif char == '\u200C':  # ZWNJ
            key.append(-99)
        elif char.isdigit():
            digit_str = char.translate(_DIGIT_CONV)
            try:
                key.append(-50 + int(digit_str))
            except ValueError:
                key.append(ord(char))
        elif char in _PERSIAN_WEIGHTS:
            key.append(_PERSIAN_WEIGHTS[char])
        else:
            key.append(ord(char))
            
    return tuple(key)


def persian_sorted(iterable: Iterable[_T], *, reverse: bool = False) -> list[_T]:
    """Sort an iterable alphabetically using correct Persian collation weights."""
    return sorted(iterable, key=persian_sort_key, reverse=reverse)  # type: ignore


def beautify_persian_spacing(text: str) -> str:
    """Optimize and beautify spaces around Persian punctuation and symbols.
    
    Carefully respects URLs, email addresses, decimal numbers (e.g. 3.14, ۱۲.۵),
    timestamps (e.g. 12:30), file names, technical identifiers, and ellipses without breaking them.
    """
    if not text:
        return text

    text, token_map = _protect_tokens(text)

    text = _PERSIAN_COMMA_RE.sub(r"\1، ", text)
    text = _PERSIAN_SEMICOLON_RE.sub(r"\1؛ ", text)

    text = _SPACE_BEFORE_PUNCT_RE.sub(r"\1", text)

    # Safe punctuation spacing: space after Persian punctuation
    text = _PERSIAN_PUNCT_SPACE_RE.sub(r"\1 ", text)
    text = _EXCLAMATION_SPACE_RE.sub(r"\1 ", text)
    text = _QUESTION_SPACE_RE.sub(r"\1 ", text)

    # Colon: space after colon when not inside a URL or between digits
    text = _COLON_SPACE_RE.sub(": ", text)

    # Period: space after period when following a Persian sentence
    text = _PERIOD_SPACE_RE.sub(". ", text)

    # Bracket, parenthesis, and guillemet spacing
    text = _OPEN_PAREN_TRIM_RE.sub("(", text)
    text = _CLOSE_PAREN_SPACE_RE.sub(")", text)
    text = _OPEN_SQBRACKET_TRIM_RE.sub("[", text)
    text = _CLOSE_SQBRACKET_TRIM_RE.sub("]", text)
    text = _OPEN_BRACE_TRIM_RE.sub("{", text)
    text = _CLOSE_BRACE_TRIM_RE.sub("}", text)
    text = _OPEN_GUILLEMET_TRIM_RE.sub("«", text)
    text = _CLOSE_GUILLEMET_TRIM_RE.sub("»", text)

    text = _OPEN_BRACKET_SPACE_RE1.sub(r"\1 (", text)
    text = _OPEN_BRACKET_SPACE_RE2.sub(r") \1", text)
    text = _OPEN_SQBRACKET_SPACE_RE1.sub(r"\1 [", text)
    text = _OPEN_SQBRACKET_SPACE_RE2.sub(r"] \1", text)
    text = _OPEN_GUILLEMET_SPACE_RE.sub(r"\1 «", text)
    text = _CLOSE_GUILLEMET_SPACE_RE.sub(r"» \1", text)

    # Re-verify no space before sentence punctuation
    text = _SPACE_BEFORE_PUNCT_RE.sub(r"\1", text)

    text = _MULTI_SPACE_PATTERN.sub(" ", text).strip()
    return _restore_tokens(text, token_map)


def extract_mobiles(text: str) -> list[str]:
    """Extract and normalize all unique Iranian mobile numbers found inside a raw text block."""
    if not text:
        return []
    
    eng_text = text.translate(_TO_ENGLISH_LOCAL)
    matches = _MOBILE_PATTERN.findall(eng_text)
    
    from parsikit.validators import normalize_mobile, is_valid_mobile
    normalized_list = []
    for match in matches:
        clean_match = re.sub(r"[\s-]", "", match)
        if is_valid_mobile(clean_match):
            normalized_list.append(normalize_mobile(clean_match, prefix="0"))
            
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
    
    eng_text = text.translate(_TO_ENGLISH_LOCAL)
    matches = _NATIONAL_CODE_PATTERN.findall(eng_text)
    
    from parsikit.validators import is_valid_national_code
    valid_codes = []
    for match in matches:
        clean_code = match.replace("-", "").replace(" ", "")
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
    """Convert Persian textual numbers (e.g. 'سی و دو هزار و پانصد') back into an integer."""
    if not text:
        return 0

    clean_text = text.replace("،", "").replace(",", "").strip()

    raw_tokens = [t.strip() for t in clean_text.split() if t.strip()]
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
        if token in _ONES:
            current_group += _ONES[token]
        elif token in _TEENS:
            current_group += _TEENS[token]
        elif token in _TENS:
            current_group += _TENS[token]
        elif token in _HUNDREDS:
            current_group += _HUNDREDS[token]
        elif token in _SCALES:
            scale = _SCALES[token]
            if scale >= 1000000 and total > 0 and total < scale:
                total = (total + current_group) * scale
                current_group = 0
            else:
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


def slugify(text: str, separator: str = "-") -> str:
    """
    Convert Persian or English text into an SEO-friendly URL slug.
    
    Transliterates Persian words to their Finglish equivalent and removes 
    special characters.
    
    E.g., "سلام دنیا" -> "salam-donya"
    """
    if not text:
        return ""

    from parsikit.number import persian_to_english

    # Normalize Persian and English characters
    cleaned = standardize_persian(text)
    cleaned = persian_to_english(cleaned).lower()

    # Extract alphanumeric tokens including Persian unicode chars
    tokens = _SLUG_TOKEN_PATTERN.findall(cleaned)

    slug_parts = []
    for token in tokens:
        # Keep pure ASCII tokens
        if token.isalnum() and token.isascii():
            slug_parts.append(token)
            continue

        # Transliterate known dictionary words
        if token in _COMMON_WORDS_PINGLISH:
            slug_parts.append(_COMMON_WORDS_PINGLISH[token])
            continue

        # Fallback to character-by-character mapping
        mapped_chars = []
        for char in token:
            if char in _CHAR_TRANS_TABLE:
                mapped_chars.append(_CHAR_TRANS_TABLE[char])
            elif char.isalnum() and char.isascii():
                mapped_chars.append(char)

        mapped_word = "".join(mapped_chars)
        if mapped_word:
            slug_parts.append(mapped_word)

    # Combine parts with separator
    raw_slug = separator.join(slug_parts)

    # Replace multiple consecutive separators with a single one
    escaped_sep = re.escape(separator)
    slug = re.sub(rf"{escaped_sep}+", separator, raw_slug)

    return slug.strip(separator)


def clean_text(text: str, *, preserve_arabic: bool = False) -> str:
    """
    Thoroughly cleanses Persian text, removing common noises, adjusting spaces,
    correcting ZWNJ layout, converting Arabic letters/numbers, and removing empty lines.
    Protects URLs, email addresses, and technical tokens from digit conversion and spacing damage.
    """
    if not text:
        return ""

    from parsikit.number import english_to_persian

    # 0. Protect URLs, emails, and technical identifiers from corruption
    text, token_map = _protect_tokens(text)

    # 1. Standardize Persian characters & Arabic transformations & NFC
    text = standardize_persian(text, preserve_arabic=preserve_arabic)

    # 2. Convert English and Arabic numbers to Persian digits (outside protected tokens)
    text = english_to_persian(text)

    # 3. Beautify spacing around punctuation
    text = beautify_persian_spacing(text)

    # 4. Remove unwanted zero-width/control characters, preserving ZWNJ (u200C)
    text = _CONTROL_CHARS_PATTERN.sub("", text)

    # 5. Collapse redundant empty lines (allows maximum 1 empty line)
    text = _REDUNDANT_NEWLINES_PATTERN.sub("\n\n", text)

    # 6. Trim leading/trailing spaces per line, and collapse extra spaces
    lines = []
    for line in text.split("\n"):
        line_cleaned = _MULTI_SPACE_PATTERN.sub(" ", line).strip()
        lines.append(line_cleaned)

    cleaned = "\n".join(lines)
    return _restore_tokens(cleaned, token_map)


def normalize_whitespace(text: str, keep_paragraphs: bool = True) -> str:
    """
    Standardize all whitespaces and line breaks in the text.
    
    Converts various Unicode spaces (excluding ZWNJ) to standard spaces, 
    clips trailing/leading margins from each line, and collapses redundant spacing.
    
    :param text: Input string.
    :param keep_paragraphs: If True, preserves single empty lines between paragraphs.
                            If False, collapses all text into a single flat line.
    :return: Cleaned and normalized text.
    """
    if not text:
        return ""

    # Convert carriage returns to Unix newlines and map non-breaking/unicode spaces to standard spaces
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = _UNICODE_SPACES_PATTERN.sub(" ", text)

    if not keep_paragraphs:
        # Convert all layout segments and newlines to simple single spaces
        text = text.replace("\n", " ")
        text = _MULTI_SPACE_PATTERN.sub(" ", text)
        return text.strip()

    # Collapse multiple consecutive newlines (3 or more) to exactly 2 newlines (1 empty line)
    text = _REDUNDANT_NEWLINES_PATTERN.sub("\n\n", text)

    # Trim leading/trailing spaces per line, and collapse extra spaces
    lines = []
    for line in text.split("\n"):
        line_cleaned = _MULTI_SPACE_PATTERN.sub(" ", line).strip()
        lines.append(line_cleaned)

    return "\n".join(lines).strip()


def convert_numbers(text: str, to: Literal["persian", "english"] = "persian") -> str:
    """
    Convert all digits inside the given text to either Persian or English script.
    
    :param text: Input string containing digits.
    :param to: Target script representation ('persian' or 'english'). Defaults to 'persian'.
    :return: Text with converted numbers.
    """
    if not text:
        return ""

    from parsikit.number import english_to_persian, persian_to_english

    target = to.lower().strip()
    if target == "persian":
        return english_to_persian(text)
    elif target == "english":
        return persian_to_english(text)
    else:
        raise ValueError("Invalid target representation style. Choose 'persian' or 'english'.")


def mask_mobile(phone: str, mask_char: str = "*") -> str:
    """
    Mask sensitive digits in an Iranian mobile phone number.
    Keeps the layout format prefix and the last 4 digits, replacing the middle with mask_char.
    E.g., "09123456789" -> "0912***6789"
    """
    if not phone:
        return ""
    cleaned = phone.strip()
    from parsikit.validators import normalize_mobile
    try:
        # Normalize to standard 09123456789 layout
        norm = normalize_mobile(cleaned, prefix="0")
        return norm[:4] + (mask_char * 3) + norm[7:]
    except ValueError:
        # Fallback if phone structure is unidentifiable
        mid = len(cleaned) // 2
        return cleaned[:max(1, mid - 2)] + (mask_char * 3) + cleaned[min(len(cleaned), mid + 2):]


def mask_card(card: str, mask_char: str = "*") -> str:
    """
    Mask sensitive digits of a 16-digit Iranian bank card number.
    Keeps the BIN prefix (first 6 digits) and last 4 digits, formatting as standard chunks.
    E.g., "6037991122334455" -> "6037-99**-****-4455"
    """
    if not card:
        return ""
    cleaned = card.strip()
    from parsikit.number import persian_to_english
    digits = "".join(c for c in persian_to_english(cleaned) if c.isdigit())
    if len(digits) == 16:
        # Mask digits from index 6 to 11 inclusive (6 digits)
        masked = digits[:6] + (mask_char * 6) + digits[12:]
        return f"{masked[:4]}-{masked[4:8]}-{masked[8:12]}-{masked[12:]}"
    # Fallback
    mid = len(cleaned) // 2
    return cleaned[:max(4, mid - 3)] + (mask_char * 6) + cleaned[min(len(cleaned), mid + 3):]


def mask_national_code(code: str, mask_char: str = "*") -> str:
    """
    Mask sensitive middle digits of an Iranian 10-digit National Code (کد ملی).
    Formats with بومی layout, keeping first 3 and last 3 digits readable.
    E.g., "7730123452" -> "773-****45-2"
    """
    if not code:
        return ""
    cleaned = code.strip()
    from parsikit.number import persian_to_english
    digits = "".join(c for c in persian_to_english(cleaned) if c.isdigit())
    if len(digits) == 10:
        masked = digits[:3] + (mask_char * 4) + digits[7:]
        return f"{masked[:3]}-{masked[3:9]}-{masked[9]}"
    # Fallback
    if len(cleaned) > 6:
        return cleaned[:3] + (mask_char * 4) + cleaned[-3:]
    return cleaned


def mask_email(email: str, mask_char: str = "*") -> str:
    """
    Mask sensitive characters in the username part of an email address.
    Keeps first 2 and last 1 character of username, masking the rest.
    E.g., "kamrani.exe@gmail.com" -> "ka********e@gmail.com"
    """
    if not email or "@" not in email:
        return email
    cleaned = email.strip()
    try:
        username, domain = cleaned.split("@", 1)
        if len(username) <= 2:
            # Mask short usernames simply
            masked_user = username[:1] + mask_char
        else:
            middle_len = len(username) - 3
            mask_len = max(3, middle_len)
            masked_user = username[:2] + (mask_char * mask_len) + username[-1:]
        return f"{masked_user}@{domain}"
    except Exception:
        return cleaned