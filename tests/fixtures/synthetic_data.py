"""
Synthetic, non-sensitive fixtures for ParsiKit test suites.
All personal data, phone numbers, cards, and national codes are strictly fictitious.
"""

# Valid synthetic Iranian National Codes with mathematically correct Modulo-11 check digits
VALID_SYNTHETIC_NATIONAL_CODES = [
    "7730123452",  # Standard test code
    "0010123458",  # Tehran (001) prefix with correct check digit 8
    "0320123456",  # Alborz (032) prefix
    "1280123451",  # Isfahan (128) prefix
]

# Invalid national codes for negative testing
INVALID_NATIONAL_CODES = [
    "1111111111",  # Repetitive digits
    "0000000000",  # All zeros
    "1234567890",  # Invalid checksum
    "7730123459",  # Wrong check digit (should be 2)
    "abcdefghij",  # Non-numeric
    "12345",       # Incomplete length
    "1234567890123", # Too long
]

# Valid synthetic mobile numbers
VALID_SYNTHETIC_MOBILES = [
    "09123456789",
    "+989123456789",
    "00989123456789",
    "989123456789",
    "۰۹۱۲۳۴۵۶۷۸۹",
    "+98۹۱۲۳۴۵۶۷۸۹",
]

# Invalid mobile numbers
INVALID_MOBILES = [
    "0912abc",
    "0912345678",    # 10 digits
    "08123456789",   # Non-mobile prefix
    "0999999999999", # Too long
    "",
]

# Synthetic 16-digit Bank Cards satisfying Luhn algorithm (using standard test BINs)
VALID_SYNTHETIC_BANK_CARDS = [
    "6037991122334455",  # Melli BIN 603799
    "6104331234567890",  # Mellat BIN 610433 (Luhn valid)
    "6219861011121315",  # Saman BIN 621986
]

INVALID_BANK_CARDS = [
    "1234",
    "6037991122334456",  # Invalid Luhn check
    "6037abcd22334455",
    "",
]

# Synthetic Sheba numbers (IR + 24 digits with valid Modulo-97 checksum)
VALID_SYNTHETIC_SHEBAS = [
    "IR050170000000123456789012",  # Melli bank code 017
    "IR320120000000001234567893",  # Mellat bank code 012
]

INVALID_SHEBAS = [
    "IR000",
    "IR050170000000123456789019",  # Invalid check digits
    "US050170000000123456789012",  # Non-IR country code
    "",
]

# Synthetic vehicle license plates
VALID_SYNTHETIC_PLATES = [
    "۱۲ ب ۳۴۵ ایران ۶۸",
    "12 ب 345 ایران 68",
    "12ب34568",
    "۲۲ الف ۱۲۳ ایران ۱۱",
]

INVALID_PLATES = [
    "invalid-plate",
    "۱۲۳ ب ۱۲۳ ایران ۱۱",
    "۱۲ ب ۳۴ ایران ۱۱",
    "",
]
