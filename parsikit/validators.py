"""
parsikit.validators
~~~~~~~~~~~~~~~~~~~
Identity, banking, and telephone format validations for Iranian standards.
"""

import re

_TO_ENGLISH = str.maketrans("۰۱۲۳۴۵۶۷۸۹٠١٢٣٤٥٦٧٨٩", "01234567890123456789")

_CARD_BIN_TO_BANK = {
    "603799": {"name": "بانک ملی ایران", "code": "melli"},
    "589210": {"name": "بانک سپه", "code": "sepah"},
    "627648": {"name": "بانک توسعه صادرات ایران", "code": "tose-saderat"},
    "627961": {"name": "بانک صنعت و معدن", "code": "sanat-o-madan"},
    "603770": {"name": "بانک کشاورزی", "code": "keshavarzi"},
    "628023": {"name": "بانک مسکن", "code": "maskan"},
    "627760": {"name": "پست بانک ایران", "code": "post-bank"},
    "502908": {"name": "بانک توسعه تعاون", "code": "tose-taavon"},
    "627412": {"name": "بانک اقتصاد نوین", "code": "eghtesad-novin"},
    "622106": {"name": "بانک پارسیان", "code": "parsian"},
    "627884": {"name": "بانک پارسیان", "code": "parsian"},
    "639194": {"name": "بانک پارسیان", "code": "parsian"},
    "639346": {"name": "بانک پاسارگاد", "code": "pasargad"},
    "502229": {"name": "بانک پاسارگاد", "code": "pasargad"},
    "627488": {"name": "بانک کارآفرین", "code": "karafarin"},
    "621986": {"name": "بانک سامان", "code": "saman"},
    "639347": {"name": "بانک سینا", "code": "sina"},
    "502806": {"name": "بانک شهر", "code": "shahr"},
    "504706": {"name": "بانک شهر", "code": "shahr"},
    "502938": {"name": "بانک دی", "code": "dey"},
    "603769": {"name": "بانک صادرات ایران", "code": "saderat"},
    "610433": {"name": "بانک ملت", "code": "mellat"},
    "991975": {"name": "بانک ملت", "code": "mellat"},
    "627353": {"name": "بانک تجارت", "code": "tejarat"},
    "585983": {"name": "بانک تجارت", "code": "tejarat"},
    "589463": {"name": "بانک رفاه کارگران", "code": "refah"},
    "636214": {"name": "بانک آینده", "code": "ayandeh"},
    "628157": {"name": "مؤسسه اعتباری توسعه", "code": "tosee"},
    "505416": {"name": "بانک گردشگری", "code": "gardeshgari"},
    "639607": {"name": "بانک سرمایه", "code": "sarmayeh"},
    "504172": {"name": "بانک قرض‌الحسنه رسالت", "code": "resalat"},
    "606373": {"name": "بانک قرض‌الحسنه مهر ایران", "code": "mehr-iran"},
    "606256": {"name": "مؤسسه اعتباری ملل", "code": "melal"},
}

_SHEBA_CODE_TO_BANK = {
    "010": {"name": "بانک مرکزی جمهوری اسلامی ایران", "code": "central-bank"},
    "011": {"name": "بانک صنعت و معدن", "code": "sanat-o-madan"},
    "012": {"name": "بانک ملت", "code": "mellat"},
    "013": {"name": "بانک رفاه کارگران", "code": "refah"},
    "014": {"name": "بانک مسکن", "code": "maskan"},
    "015": {"name": "بانک سپه", "code": "sepah"},
    "016": {"name": "بانک کشاورزی", "code": "keshavarzi"},
    "017": {"name": "بانک ملی ایران", "code": "melli"},
    "018": {"name": "بانک تجارت", "code": "tejarat"},
    "019": {"name": "بانک صادرات ایران", "code": "saderat"},
    "020": {"name": "بانک توسعه صادرات ایران", "code": "tose-saderat"},
    "021": {"name": "پست بانک ایران", "code": "post-bank"},
    "022": {"name": "بانک توسعه تعاون", "code": "tose-taavon"},
    "051": {"name": "مؤسسه اعتباری توسعه", "code": "tosee"},
    "052": {"name": "بانک سپه (قوامین سابق)", "code": "sepah"},
    "053": {"name": "بانک کارآفرین", "code": "karafarin"},
    "054": {"name": "بانک پارسیان", "code": "parsian"},
    "055": {"name": "بانک سامان", "code": "saman"},
    "056": {"name": "بانک پاسارگاد", "code": "pasargad"},
    "057": {"name": "بانک گردشگری", "code": "gardeshgari"},
    "058": {"name": "بانک سرمایه", "code": "sarmayeh"},
    "059": {"name": "بانک سینا", "code": "sina"},
    "060": {"name": "بانک قرض‌الحسنه مهر ایران", "code": "mehr-iran"},
    "061": {"name": "بانک شهر", "code": "shahr"},
    "062": {"name": "بانک آینده", "code": "ayandeh"},
    "063": {"name": "بانک دی", "code": "dey"},
    "064": {"name": "بانک سپه (حکمت سابق)", "code": "sepah"},
    "065": {"name": "مؤسسه اعتباری توسعه صنعت و تجارت", "code": "tosee-sanat-o-tejarat"},
    "066": {"name": "بانک سپه (انصار سابق)", "code": "sepah"},
    "069": {"name": "بانک ایران زمین", "code": "iran-zamin"},
    "070": {"name": "بانک سپه (مهر اقتصاد سابق)", "code": "sepah"},
    "073": {"name": "بانک سپه (کوثر سابق)", "code": "sepah"},
    "075": {"name": "مؤسسه اعتباری ملل", "code": "melal"},
    "078": {"name": "بانک خاورمیانه", "code": "khavarmiyaneh"},
    "079": {"name": "بانک مشترک ایران و ونزوئلا", "code": "iran-venezuela"},
    "080": {"name": "بانک قرض‌الحسنه رسالت", "code": "resalat"},
}

_BILL_TYPES = {
    "1": "آب", "2": "برق", "3": "گاز", "4": "تلفن ثابت",
    "5": "تلفن همراه", "6": "عوارض شهرداری", "7": "سازمان مالیاتی", "8": "جرایم راهنمایی و رانندگی"
}

_PROVINCE_CODES = {
    "11": "تهران", "22": "تهران", "33": "تهران", "44": "تهران", "55": "تهران",
    "66": "تهران", "77": "تهران", "88": "تهران", "99": "تهران", "10": "تهران",
    "20": "تهران", "30": "تهران", "40": "تهران", "50": "تهران", "60": "تهران",
    "90": "تهران",
    "12": "خراسان رضوی", "32": "خراسان رضوی", "42": "خراسان رضوی", "36": "خراسان رضوی", "74": "خراسان رضوی",
    "13": "اصفهان", "23": "اصفهان", "43": "اصفهان", "53": "اصفهان", "67": "اصفهان",
    "14": "خوزستان", "24": "خوزستان", "34": "خوزستان",
    "15": "آذربایجان شرقی", "25": "آذربایجان شرقی", "35": "آذربایجان شرقی",
    "16": "قم",
    "17": "آذربایجان غربی", "27": "آذربایجان غربی", "37": "آذربایجان غربی",
    "18": "همدان", "28": "همدان",
    "19": "کرمانشاه", "29": "کرمانشاه", "39": "کرمانشاه",
    "21": "البرز", "38": "البرز", "68": "البرز", "78": "البرز",
    "26": "خراسان شمالی",
    "31": "لرستان", "41": "لرستان",
    "45": "کرمان", "65": "کرمان", "75": "کرمان",
    "46": "گیلان", "56": "گیلان", "76": "گیلان",
    "47": "مرکزی", "57": "مرکزی",
    "48": "بوشهر", "58": "بوشهر",
    "49": "کهگیلویه و بویراحمد",
    "51": "کردستان", "61": "کردستان",
    "52": "خراسان جنوبی",
    "54": "یزد", "64": "یزد",
    "59": "گلستان", "69": "گلستان",
    "62": "مازندران", "72": "مازندران", "82": "مازندران", "92": "مازندران",
    "71": "چهارمحال و بختیاری", "81": "چهارمحال و بختیاری",
    "79": "قزوین", "89": "قزوین",
    "84": "هرمزگان", "94": "هرمزگان",
    "85": "سیستان و بلوچستان", "95": "سیستان و بلوچستان",
    "86": "سمنان", "96": "سمنان",
    "87": "زنجان", "97": "زنجان",
    "91": "اردبیل",
    "98": "ایلام",
}

_PLATE_CATEGORIES = {
    "ت": "تاکسی",
    "ع": "عمومی",
    "الف": "دولتی",
    "پ": "پلیس",
    "ث": "سپاه پاسداران",
    "ش": "ارتش جمهوری اسلامی ایران",
    "ز": "وزارت دفاع",
    "ف": "ستاد کل نیروهای مسلح",
    "ک": "ادوات کشاورزی",
    "گ": "گذر موقت",
    "ژ": "جانبازان و معلولین",
    "D": "سیاسی",
    "S": "سرویس سفارتخانه",
}


def is_valid_national_code(code: str) -> bool:
    """Check if the provided code is a valid 10-digit Iranian National Code (auto-pads omitted leading zeros)."""
    if not code:
        return False

    clean = "".join(c for c in str(code).translate(_TO_ENGLISH) if c.isdigit())

    if len(clean) < 10:
        clean = clean.zfill(10)
    elif len(clean) > 10:
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
    """Standardize mobile formats to specified layout prefixes (e.g., '0', '+98', '98', '0098', or empty bare '')."""
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
    elif prefix == "0098":
        return f"0098{base}"
    elif prefix == "":
        return base
    
    raise ValueError("Unsupported prefix format. Choose '0', '+98', '98', '0098', or ''.")


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
    """Validate Iranian Sheba (IBAN) format (starts with IR followed by 24 digits, handles all custom separators)."""
    if not sheba:
        return False
    
    # Extract only alphanumeric characters to make it immune to various formatting symbols
    clean = "".join(c for c in str(sheba).translate(_TO_ENGLISH).upper() if c.isdigit() or ('A' <= c <= 'Z'))

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
    clean = "".join(c for c in str(sheba).translate(_TO_ENGLISH).upper() if c.isdigit() or ('A' <= c <= 'Z'))

    if len(clean) == 24 and clean.isdigit():
        clean = "IR" + clean

    if len(clean) != 26 or not clean.startswith("IR") or not clean[2:].isdigit():
        raise ValueError("Invalid Sheba structure.")

    if format_type == "clean":
        return clean

    # spaced chunk format
    return " ".join([clean[i:i+4] for i in range(0, 26, 4)])


def is_valid_corporate_id(code: str) -> bool:
    """Validate 11-digit Iranian Legal Entity National ID (شناسه ملی اشخاص حقوقی)."""
    if not code:
        return False
    
    clean = "".join(c for c in str(code).translate(_TO_ENGLISH) if c.isdigit())
    
    if len(clean) != 11:
        return False
        
    # Exclude repeating single digit IDs (e.g., 11111111111)
    if len(set(clean)) == 1:
        return False
        
    d = int(clean[9]) + 2
    z = [29, 27, 23, 19, 17]
    s = sum((int(clean[i]) + d) * z[i % 5] for i in range(10))
    rem = s % 11
    if rem == 10:
        rem = 0
    
    check_digit = int(clean[10])
    return check_digit == rem


def detect_mobile_operator(phone: str) -> str | None:
    """Detect the telecom operator of an Iranian mobile phone number."""
    try:
        normalized = normalize_mobile(phone, prefix="0")
    except ValueError:
        return None
        
    prefix = normalized[:4]
    
    mci_prefixes = {
        "0910", "0911", "0912", "0913", "0914", "0915", "0916", "0917", "0918", "0919",
        "0990", "0991", "0992", "0993", "0994", "0996"
    }
    irancell_prefixes = {
        "0930", "0933", "0935", "0936", "0937", "0938", "0939",
        "0901", "0902", "0903", "0904", "0905", "0900", "0941"
    }
    rightel_prefixes = {"0920", "0921", "0922", "0923"}
    shatel_prefixes = {"0998"}
    samantel_prefixes = {"0999"}
    taliya_prefixes = {"0932"}
    tkc_prefixes = {"0934"}
    
    if prefix in mci_prefixes:
        return "MCI"
    elif prefix in irancell_prefixes:
        return "Irancell"
    elif prefix in rightel_prefixes:
        return "RighTel"
    elif prefix in shatel_prefixes:
        return "Shatel Mobile"
    elif prefix in samantel_prefixes:
        return "SamanTel"
    elif prefix in taliya_prefixes:
        return "Taliya"
    elif prefix in tkc_prefixes:
        return "TKC"
        
    return None


def detect_bank_from_card(card: str) -> dict | None:
    """Detect the bank details from a 16-digit card number or its 6-digit prefix (BIN)."""
    if not card:
        return None
    clean = "".join(c for c in str(card).translate(_TO_ENGLISH) if c.isdigit())
    if len(clean) < 6:
        return None
    return _CARD_BIN_TO_BANK.get(clean[:6])


def detect_bank_from_sheba(sheba: str) -> dict | None:
    """Detect the bank details from a Sheba (IBAN) code or its prefix."""
    if not sheba:
        return None
    clean = "".join(c for c in str(sheba).translate(_TO_ENGLISH).upper() if c.isdigit() or ('A' <= c <= 'Z'))
    if len(clean) == 24 and clean.isdigit():
        clean = "IR" + clean
    if len(clean) < 7 or not clean.startswith("IR"):
        return None
    bank_code = clean[4:7]
    return _SHEBA_CODE_TO_BANK.get(bank_code)


def is_valid_postal_code(postal_code: str) -> bool:
    """Validate 10-digit Iranian Postal Code."""
    if not postal_code:
        return False
    clean = "".join(c for c in str(postal_code).translate(_TO_ENGLISH) if c.isdigit())
    if len(clean) != 10:
        return False
    first_five = clean[:5]
    if '0' in first_five or '2' in first_five:
        return False
    return True


def format_postal_code(postal_code: str) -> str:
    """Format postal code cleanly as XXXXX-XXXXX."""
    clean = "".join(c for c in str(postal_code).translate(_TO_ENGLISH) if c.isdigit())
    if len(clean) != 10:
        raise ValueError("Postal code must contain exactly 10 digits.")
    return f"{clean[:3]}-{clean[3:9]}-{clean[9]}"


def _calculate_mod11_bill_checksum(digits_str: str) -> int:
    """Calculate modulo 11 checksum for Iranian bills."""
    weights = [2, 3, 4, 5, 6, 7]
    total = 0
    for i, char in enumerate(reversed(digits_str)):
        weight = weights[i % 6]
        total += int(char) * weight
    rem = total % 11
    if rem == 0 or rem == 1:
        return 0
    return 11 - rem


def is_valid_bill_and_payment(bill_id: str, pay_id: str) -> bool:
    """Validate Iranian Bill ID and Payment ID using standard Modulo 11 check digits."""
    _TO_ENGLISH_LOCAL = str.maketrans("۰۱۲۳۴۵۶۷۸۹٠١٢٣٤٥٦٧٨٩", "01234567890123456789")
    b = "".join(c for c in str(bill_id).translate(_TO_ENGLISH_LOCAL) if c.isdigit())
    p = "".join(c for c in str(pay_id).translate(_TO_ENGLISH_LOCAL) if c.isdigit())
    
    if len(b) < 6 or len(p) < 6:
        return False
        
    # Check 1: Bill ID check digit
    if _calculate_mod11_bill_checksum(b[:-1]) != int(b[-1]):
        return False
        
    # Check 2: Payment ID first check digit (Control 1)
    if _calculate_mod11_bill_checksum(p[:-2]) != int(p[-2]):
        return False
        
    # Check 3: Combined check digit (Control 2)
    combined = b.lstrip('0') + p[:-1].lstrip('0')
    if _calculate_mod11_bill_checksum(combined) != int(p[-1]):
        return False
        
    return True


def extract_bill_details(bill_id: str, pay_id: str) -> dict | None:
    """Validate and extract payment details and type from Iranian Bill & Payment IDs."""
    _TO_ENGLISH_LOCAL = str.maketrans("۰۱۲۳۴۵۶۷۸۹٠١٢٣٤٥٦٧٨٩", "01234567890123456789")
    b = "".join(c for c in str(bill_id).translate(_TO_ENGLISH_LOCAL) if c.isdigit())
    p = "".join(c for c in str(pay_id).translate(_TO_ENGLISH_LOCAL) if c.isdigit())
    
    if len(b) < 6 or len(p) < 6:
        return None
        
    is_valid = is_valid_bill_and_payment(b, p)
    
    type_code = b[-2]
    bill_type = _BILL_TYPES.get(type_code, "سایر قبوض")
    
    amount_base_str = p[:-2]
    try:
        amount_base = int(amount_base_str)
        amount_rial = amount_base * 1000
        amount_toman = amount_rial // 10
    except ValueError:
        amount_rial = 0
        amount_toman = 0
        
    return {
        "is_valid": is_valid,
        "amount_rial": amount_rial,
        "amount_toman": amount_toman,
        "type": bill_type,
        "type_code": type_code,
    }


def parse_plate(plate_str: str) -> dict | None:
    """Parse an Iranian National Vehicle Plate (پلاک ملی) and extract details.
    
    Returns a dict with:
        - part1 (str): First 2 digits (e.g., "۱۲")
        - letter (str): Middle letter/character (e.g., "ب", "الف")
        - part2 (str): 3 digits (e.g., "۳۴۵")
        - province_code (str): Province numeric code (e.g., "۶۸")
        - province (str): Issuing Persian province name (e.g., "البرز")
        - category (str): Car type category (e.g., "شخصی", "تاکسی")
    Or None if the plate structure is invalid.
    """
    _TO_ENGLISH_LOCAL = str.maketrans("۰۱۲۳۴۵۶۷۸۹٠١٢٣٤٥٦٧٨٩", "01234567890123456789")
    s = str(plate_str).translate(_TO_ENGLISH_LOCAL).strip()
    s = s.replace("ایران", "").replace("-", "").replace(" ", "")
    
    plate_regex = re.compile(r"^(\d{2})([بجدسصطقلمنوهیتعپثشزفکگژDS]|الف)(\d{3})(\d{2})$")
    match = plate_regex.match(s)
    if not match:
        return None
        
    p1, letter, p2, p3 = match.groups()
    category = _PLATE_CATEGORIES.get(letter, "شخصی")
    province = _PROVINCE_CODES.get(p3, "نامشخص")
    
    _TO_PERSIAN_LOCAL = str.maketrans("0123456789", "۰۱۲۳۴۵۶۷۸۹")
    p1_fa = p1.translate(_TO_PERSIAN_LOCAL)
    p2_fa = p2.translate(_TO_PERSIAN_LOCAL)
    p3_fa = p3.translate(_TO_PERSIAN_LOCAL)
    
    return {
        "part1": p1_fa,
        "letter": letter,
        "part2": p2_fa,
        "province_code": p3_fa,
        "province": province,
        "category": category,
    }


def is_valid_plate(plate_str: str) -> bool:
    """Check if the given string is a structurally valid Iranian Vehicle Plate."""
    return parse_plate(plate_str) is not None


def format_plate(plate_str: str, format_type: str = "readable") -> str:
    """Format an Iranian Vehicle Plate into a standard readable or clean layout."""
    parsed = parse_plate(plate_str)
    if not parsed:
        raise ValueError(f"Invalid Iranian plate structure '{plate_str}'")
        
    if format_type == "clean":
        return f"{parsed['part1']}{parsed['letter']}{parsed['part2']}{parsed['province_code']}"
        
    return f"{parsed['part1']} {parsed['letter']} {parsed['part2']} - ایران {parsed['province_code']}"