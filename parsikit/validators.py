"""
parsikit.validators
~~~~~~~~~~~~~~~~~~~
Identity, banking, and telephone format validations for Iranian standards.
"""

import re

_TO_ENGLISH = str.maketrans("۰۱۲۳۴۵۶۷۸۹٠١٢٣٤٥٦٧٨٩", "01234567890123456789")


def is_valid_national_code(code: str) -> bool:
    """Check if the provided code is a valid 10-digit Iranian National Code."""
    if not code:
        return False

    clean = "".join(c for c in str(code).translate(_TO_ENGLISH) if c.isdigit())

    if len(clean) != 10:
        return False

    # Block patterns with repeating single digits (e.g., 1111111111)
    if len(set(clean)) == 1:
        return False

    digits = [int(d) for d in clean]
    check_digit = digits[-1]

    s = sum(digits[i] * (10 - i) for i in range(9))
    r = s % 11

    if r < 2:
        return check_digit == r
    
    return check_digit == (11 - r)


def format_national_code(code: str) -> str:
    """Format national code into standardized format (e.g. XXX-XXXXXX-X)."""
    clean = "".join(c for c in str(code).translate(_TO_ENGLISH) if c.isdigit())
    
    if len(clean) < 10:
        clean = clean.zfill(10)
    elif len(clean) > 10:
        raise ValueError("National code must not exceed 10 digits.")
        
    return f"{clean[:3]}-{clean[3:9]}-{clean[9]}"


def is_valid_mobile(phone: str) -> bool:
    """Validate Iranian mobile numbers (supports +98, 0098, 98, 0 and bare prefixes)."""
    if not phone:
        return False
    clean = "".join(c for c in str(phone).translate(_TO_ENGLISH) if c.isdigit() or c == "+")
    pattern = re.compile(r"^(?:\+98|0098|98|0)?9\d{9}$")
    return bool(pattern.match(clean))


def normalize_mobile(phone: str, prefix: str = "0") -> str:
    """Standardize mobile formats to specified layout prefixes (e.g., '0', '+98', '98')."""
    if not is_valid_mobile(phone):
        raise ValueError("Invalid Iranian mobile number layout.")
        
    clean = "".join(c for c in str(phone).translate(_TO_ENGLISH) if c.isdigit())
    base = clean[-10:]
    
    if prefix == "0":
        return f"0{base}"
    elif prefix == "+98":
        return f"+98{base}"
    elif prefix == "98":
        return f"98{base}"
    
    raise ValueError("Unsupported prefix format. Choose '0', '+98', or '98'.")


def is_valid_card_number(card: str) -> bool:
    """Validate 16-digit bank card numbers using Luhn checksum algorithm."""
    if not card:
        return False
    clean = "".join(c for c in str(card).translate(_TO_ENGLISH) if c.isdigit())
    
    if len(clean) != 16:
        return False
        
    digits = [int(x) for x in clean]
    for i in range(0, 16, 2):
        val = digits[i] * 2
        if val > 9:
            val -= 9
        digits[i] = val
        
    return sum(digits) % 10 == 0


def format_card_number(card: str, separator: str = "-") -> str:
    """Format bank card numbers into standard four-chunk groups."""
    clean = "".join(c for c in str(card).translate(_TO_ENGLISH) if c.isdigit())
    if len(clean) != 16:
        raise ValueError("Card number must contain exactly 16 digits.")
    return separator.join([clean[i:i+4] for i in range(0, 16, 4)])


def is_valid_sheba(sheba: str) -> bool:
    """Validate Iranian Sheba (IBAN) format (starts with IR followed by 24 digits)."""
    if not sheba:
        return False
    
    clean = str(sheba).translate(_TO_ENGLISH).upper().replace(" ", "").replace("-", "")

    if len(clean) == 24 and clean.isdigit():
        clean = "IR" + clean

    if len(clean) != 26 or not clean.startswith("IR") or not clean[2:].isdigit():
        return False

    # Move 'IRXX' to end: 'IRXXYYYY...' -> 'YYYY...IRXX'
    rearranged = clean[4:] + clean[:4]
    
    # Translate letters to numbers (I -> 18, R -> 27)
    num_str = ""
    for char in rearranged:
        if char.isalpha():
            num_str += str(ord(char) - ord('A') + 10)
        else:
            num_str += char

    try:
        return int(num_str) % 97 == 1
    except ValueError:
        return False


def format_sheba(sheba: str, format_type: str = "spaced") -> str:
    """Format Sheba values cleanly or into four-character readable blocks."""
    clean = str(sheba).translate(_TO_ENGLISH).upper().replace(" ", "").replace("-", "")

    if len(clean) == 24 and clean.isdigit():
        clean = "IR" + clean

    if len(clean) != 26 or not clean.startswith("IR") or not clean[2:].isdigit():
        raise ValueError("Invalid Sheba structure.")

    if format_type == "clean":
        return clean

    # spaced chunk format
    return " ".join([clean[i:i+4] for i in range(0, 26, 4)])