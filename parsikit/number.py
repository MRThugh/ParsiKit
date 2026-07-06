"""
parsikit.number
~~~~~~~~~~~~~~~
Number conversion utilities and textual representations of numbers.
"""

from __future__ import annotations
from parsikit.cache import memoize

_TO_PERSIAN_TABLE = str.maketrans(
    {
        "0": "\u06F0", "1": "\u06F1", "2": "\u06F2",
        "3": "\u06F3", "4": "\u06F4", "5": "\u06F5",
        "6": "\u06F6", "7": "\u06F7", "8": "\u06F8",
        "9": "\u06F9",
        "\u0660": "\u06F0", "\u0661": "\u06F1", "\u0662": "\u06F2",
        "\u0663": "\u06F3", "\u0664": "\u06F4", "\u0665": "\u06F5",
        "\u0666": "\u06F6", "\u0667": "\u06F7", "\u0668": "\u06F8",
        "\u0669": "\u06F9",
    }
)

_TO_ENGLISH_TABLE = str.maketrans(
    {
        "\u06F0": "0", "\u06F1": "1", "\u06F2": "2",
        "\u06F3": "3", "\u06F4": "4", "\u06F5": "5",
        "\u06F6": "6", "\u06F7": "7", "\u06F8": "8",
        "\u06F9": "9",
        "\u0660": "0", "\u0661": "1", "\u0662": "2",
        "\u0663": "3", "\u0664": "4", "\u0665": "5",
        "\u0666": "6", "\u0667": "7", "\u0668": "8",
        "\u0669": "9",
    }
)


def english_to_persian(text: str) -> str:
    """Convert English/Arabic digits inside a string to Persian equivalents."""
    if not text:
        return text
    return text.translate(_TO_PERSIAN_TABLE)


def persian_to_english(text: str) -> str:
    """Convert Persian/Arabic digits inside a string to English equivalents."""
    if not text:
        return text
    return text.translate(_TO_ENGLISH_TABLE)


@memoize(maxsize=1024)
def number_to_words(number: int | str) -> str:
    """Convert numeric values to written Persian words."""
    if isinstance(number, str):
        clean_num = number.replace(",", "").replace("،", "").replace(" ", "")
        clean_num = clean_num.translate(_TO_ENGLISH_TABLE)
        try:
            num = int(clean_num)
        except ValueError:
            raise ValueError(f"Cannot convert '{number}' to a valid integer.") from None
    else:
        num = int(number)

    if num == 0:
        return "صفر"

    is_negative = False
    if num < 0:
        is_negative = True
        num = abs(num)

    ones = {
        1: "یک", 2: "دو", 3: "سه", 4: "چهار", 5: "پنج",
        6: "شش", 7: "هفت", 8: "هشت", 9: "نه"
    }
    tens = {
        10: "ده", 11: "یازده", 12: "دوازده", 13: "سیزده", 14: "چهارده",
        15: "پانزده", 16: "شانزده", 17: "هفده", 18: "هجده", 19: "نوزده"
    }
    twenties = {
        2: "بیست", 3: "سی", 4: "چهل", 5: "پنجاه",
        6: "شصت", 7: "هفتاد", 8: "هشتاد", 9: "نود"
    }
    hundreds = {
        1: "یکصد", 2: "دویست", 3: "سیصد", 4: "چهارصد", 5: "پانصد",
        6: "ششصد", 7: "هفتصد", 8: "هشتصد", 9: "نهصد"
    }
    thousands = [
        "", "هزار", "میلیون", "میلیارد", "تریلیون", "کوآدریلیون",
        "کوئینتیلیون", "سکستیلیون", "سپتیلیون"
    ]

    def _convert_group(n: int) -> str:
        parts = []
        h = n // 100
        t_o = n % 100
        
        if h > 0:
            parts.append(hundreds[h])
            
        if t_o > 0:
            if 10 <= t_o <= 19:
                parts.append(tens[t_o])
            else:
                t = t_o // 10
                o = t_o % 10
                if t > 0:
                    parts.append(twenties[t])
                if o > 0:
                    parts.append(ones[o])
                    
        return " و ".join(parts)

    chunks = []
    temp = num
    while temp > 0:
        chunks.append(temp % 1000)
        temp //= 1000

    if len(chunks) > len(thousands):
        raise ValueError("Number is too large to convert to words. Maximum supported is 999 septillion.")

    words_list = []
    for i, chunk in enumerate(chunks):
        if chunk > 0:
            chunk_word = _convert_group(chunk)
            unit = thousands[i]
            if unit:
                if i == 1 and chunk == 1:
                    words_list.append(unit)
                else:
                    words_list.append(f"{chunk_word} {unit}".strip())
            else:
                words_list.append(chunk_word)

    words_list.reverse()
    result = " و ".join(words_list)
    
    if is_negative:
        result = "منفی " + result
        
    return result