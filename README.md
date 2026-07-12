<div align="center">

# 🌟 ParsiKit Library 🌟
<p align="center">
  <img 
    src="https://raw.githubusercontent.com/MRThugh/MRThugh/main/badge.svg"
    width="50%" 
  />
</p>

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Author](https://img.shields.io/badge/author-Ali%20Kamrani-purple.svg)](https://github.com/MRThugh)
[![Version](https://img.shields.io/badge/version-3.3.0-blue.svg)](https://github.com/MRThugh/ParsiKit)
[![Persian](https://img.shields.io/badge/lang-PERSIAN-green)](README-fa.md)
[![English](https://img.shields.io/badge/lang-English-blue)](README.md)

**A production-grade, highly performant, and pure Python software infrastructure for Persian text processing, validation, financial calculations, calendar conversions, graphical text reshaping, developer diagnostics, and sensitive data security.**

</div>

---

## 📖 Overview

**ParsiKit** (imported as `parsikit`) is a robust, zero-dependency Python library designed as a full-scale infrastructure for Persian language applications.

With the release of **v3.3.0**, ParsiKit evolves into a highly advanced developer utility, text-cleansing, and security-centric suite. Alongside its unified procedural API and rich **Object-Oriented Domain Model**, ParsiKit now introduces bومی (Persian-aware) formatting, visual alignment helpers, text diagnostics, smart classifiers, and sensitive data masking tools designed to make Persian software development reliable, clean, and secure.

---

## 🚀 Key Architectural Pillars in v3.3.0

### 1. Unified Configuration & Thread-Safe Caching (`parsikit.config`, `parsikit.cache`)
* **Thread-Safe Caching**: Highly repetitive and CPU-bound operations (such as converting large digits to words or parsing database dates) are optimized with an internal thread-safe LRU-like cache.
* **Global Configurations**: Easily control default parameters like value-added tax rates, default currency units, or toggle caching on/off dynamically at runtime.

### 2. Custom Structured Exceptions (`parsikit.exceptions`)
Never worry about managing generic `ValueError` or `TypeError` crashes. ParsiKit ships with a structured exception tree tailored to Iranian standards, making it perfect for Clean Architecture or DDD pipelines.

### 3. Object-Oriented Domain Models (`parsikit.models`)
Wrap raw strings in rich domain models like `PersianText`, `NationalCode`, `MobileNumber`, `FixedLine`, `BankCard`, `Sheba`, or `VehiclePlate`. These models validate inputs upon instantiation, extract rich metadata (like province/city of issue, operators, or bank details), and serialize cleanly.

### 4. Developer Diagnostics & bومی Formatting (`parsikit.dev` - New in v3.3.0!)
* **Persian-Aware Visual Padding (`pformat` & `persian_fstring`)**: Standard formatters misalign texts containing Zero-Width Non-Joiners (ZWNJs) or Arabic diacritics. ParsiKit calculates true visual string widths to output cleanly aligned tables and logs, supporting automatic Persian digit conversions.
* **Interactive Text Debugging**: Inspect texts for missing ZWNJs, layout issues, or redundant spacings and get immediate corrective actions.

### 5. Advanced SEO, Sanitization, & Security Suite (New in v3.3.0!)
* **SEO Romanization (`slugify`)**: Transliterates mixed or Persian strings into SEO-friendly Finglish slugs, utilizing a built-in common word mapping dictionary.
* **Master Cleansing & Normalization (`clean_text` / `normalize_whitespace`)**: Sanitize multi-line texts by eliminating hidden unicode characters, collapsing redundant whitespace, correcting ZWNJ boundaries, and resolving newline excesses.
* **Smart Data Detection (`detect`)**: A unified classifier that parses strings to automatically identify if they represent an Iranian mobile number, national code, card number, Sheba code, email, URL, or IP address.
* **Sensitive Data Masking (`mask_*`)**: Instantly scrub logs, API outputs, or admin panel displays by masking middle digits of mobiles, cards, emails, and national codes.

---

## ⚙️ Installation

```bash
pip install parsikit
```

**Requires Python 3.10+**

---

## 🛠️ Configuration & Exception Management

### 1. Global Configurations
```python
import parsikit

# Adjust VAT/Tax rate globally (Default: 0.10)
parsikit.config.default_tax_rate = 0.09

# Adjust global default currency (Default: "toman")
parsikit.config.default_currency = "rial"

# Toggle high-performance computation caching
parsikit.config.enable_cache = True
```

### 2. Exception Hierarchy
All specific exceptions inherit from `parsikit.exceptions.ValidationError` which inherits from `ParsiKitError` and Python's native `ValueError`:
```python
import parsikit

try:
    card = parsikit.BankCard("invalid-card-number")
except parsikit.InvalidCardNumberError as e:
    print(f"Card processing failed: {e}")
except parsikit.ValidationError as e:
    print(f"Generic ParsiKit validation error: {e}")
```

---

## 🦄 Native Pydantic v2 & FastAPI Integration

You can declare ParsiKit models directly inside Pydantic schemas or FastAPI route handlers. ParsiKit natively handles data parsing, raises clean structured validation errors on failure, and serializes values cleanly to string:

```python
from fastapi import FastAPI
from pydantic import BaseModel
import parsikit

app = FastAPI()

class UserRegisterSchema(BaseModel):
    fullname: parsikit.PersianText
    national_id: parsikit.NationalCode
    phone: parsikit.MobileNumber
    card: parsikit.BankCard

@app.post("/register")
def register_user(user: UserRegisterSchema):
    # Inputs are already parsed, validated, and normalized!
    print(user.fullname.standardize()) # Normalized chain
    print(user.national_id.location)   # {"province": "تهران", "city": "تهران مرکزی"}
    print(user.phone.to_international()) # "+989123456789"
    
    # Easily serialize everything to dictionary
    return {
        "status": "success",
        "data": {
            "national_id": user.national_id.to_dict(),
            "card_bank": user.card.bank
        }
    }
```

---

## 🚀 Feature Guides & Code Examples

### 1. Developer Diagnostics Ecosystem (`parsikit.dev`)
ParsiKit v3.3.0 ships with a highly optimized developer diagnostic suite for printing, inspecting, and managing logs containing Persian data.

#### Interactive Text Diagnostics
Identify encoding errors, missing semi-spaces, or digit script issues instantly:
```python
import parsikit

# Get detailed dictionary diagnostics
analysis = parsikit.inspect_text("ي كافيه ك کتاب ها ميباشد ۱۲۳")
print(analysis["has_arabic_chars"]) # True
print(analysis["has_zwnj_issues"])  # True
print(analysis["suggestions"])
# Output: [
#   "Replace Arabic letters (ي, ك, ة) with standard Persian equivalents (ی, ک, ه).",
#   "Add proper zero-width non-joiners (ZWNJs) around prefixes/suffixes.",
#   ...
# ]

# Print a beautiful terminal-colored diagnostic report to stdout
parsikit.debug_text("ي كافيه ك کتاب ها ميباشد")
```

#### Smart Pretty Printing & Native Container Repr
Standard Python structures escape Persian characters inside containers. ParsiKit fixes this with native-repr representations and colored outputs:
```python
import parsikit

data = {"کاربر": ["امیر", "رضا"], "وضعیت": True}

# Standard python repr: "{'\\u06a9\\u0627\\u0631\\u0628\\u0631': ['\\u0627\\u0645\\u06cc\\u0631', ...]}"
# ParsiKit clean representation:
print(parsikit.persian_repr(data))
# Output: {'کاربر': ['امیر', 'رضا'], 'وضعیت': True}

# Pretty print structured dicts/lists or ParsiKit models with ANSI colors
parsikit.pretty_print(data, title="User Information")
```

#### Batch Validation Reports
Validate batches of raw inputs against any ParsiKit domain model and print/return a summary breakdown:
```python
import parsikit

items = ["7730123452", "1111111111", "0010123451", "bad-code"]
report = parsikit.validate_batch(items, parsikit.NationalCode, silent=False)
# Prints a structured validation summary detailing valid/invalid elements and indexes
```

#### Raw Persian Logging Setup
Configures Python's stream logger with clean formatting that prints unescaped Persian text:
```python
import parsikit

logger = parsikit.setup_logging("DEBUG")
logger.info("ثبت نام کاربر با موفقیت انجام شد.")
```

---

### 2. Persian-Aware Text Formatting (`pformat` & `persian_fstring`)
Standard string formatters align strings based on character length. However, zero-width characters (like ZWNJs) or diacritics occupy character indices while taking up zero visual width, resulting in crooked alignments. ParsiKit resolves this visually.

#### Clean Padding with Zero-Width Characters
```python
import parsikit

# "کتاب‌‌ها" contains a ZWNJ (character length is 8, but visually occupies 7 slots)
# Standard format '{:<10}' outputs a string with 2 trailing spaces (visual width of 9)
# pformat compensates for the ZWNJ, adding 3 trailing spaces to achieve a visual width of exactly 10 slots:
aligned = parsikit.pformat("{:<10} | تراز شد", "کتاب‌‌ها")
print(aligned) # "کتاب‌‌ها   | تراز شد"
```

#### Suffix-Based Digit Conversion
Append `:fa` or `:p` to placeholders inside templates to automatically format numbers in Persian script:
```python
import parsikit

# Auto convert numbers to Persian digits and apply standard spacing/grouping
print(parsikit.pformat("هزینه: {:>10,fa} ریال", 1500000))
# Output: "هزینه:  ۱،۵۰۰،۰۰۰ ریال"
```

#### Contextual f-string Evaluator
Evaluates standard formatting templates while automatically extracting local/global variables from the caller's frame context:
```python
import parsikit

name = "علی"
price = 12500

# Automatically parses 'name' and 'price' from the surrounding variables scope
formatted = parsikit.persian_fstring("کاربر: {name:<5} | قیمت: {price:fa} تومان")
print(formatted)
# Output: "کاربر: علی   | قیمت: ۱۲۵۰۰ تومان"
```

---

### 3. SEO, Whitespace, & Cleansing Suite
Easily convert mixed Persian scripts into clean components, URLs, and database-safe records.

#### Finglish SEO Slug Generator
Transliterates mixed or Persian strings into SEO-friendly, clean Finglish slugs:
```python
import parsikit

# Auto maps popular Persian words (like "سلام" -> "salam", "دنیا" -> "donya", "آموزش" -> "amoozesh")
# and transliterates other characters alphabetically
print(parsikit.slugify("آموزش وردپرس به زبان ساده"))
# Output: "amoozesh-wordpress-beh-zaban-sadeh"

print(parsikit.slugify("سلام دنیا 💕"))
# Output: "salam-donya"
```

#### Master Text Sanitizer
Removes invisible non-printing unicode characters, collapses extra spaces, fixes ZWNJ boundaries, and converts Arabic characters and English digits:
```python
import parsikit

dirty_text = "ي كافيه ك   کتاب  ها  ميباشد  ۱۱۲۳\n\n\n\nجدید  "
print(parsikit.clean_text(dirty_text))
# Output:
# "ی کافیه ک کتاب‌ها میباشد ۱۱۲۳
# 
# جدید"
```

#### Whitespace Normalizer
Normalizes whitespace structures, with an option to preserve single paragraph line breaks or flatten them into a single line:
```python
import parsikit

raw_paragraphs = "خط اول\n\n\n\nخط دوم   با   فاصله\n\nخط سوم"

# Preserves paragraph spacing
print(parsikit.normalize_whitespace(raw_paragraphs, keep_paragraphs=True))
# Output:
# "خط اول
# 
# خط دوم با فاصله
# 
# خط سوم"

# Flattens all line breaks
print(parsikit.normalize_whitespace(raw_paragraphs, keep_paragraphs=False))
# Output: "خط اول خط دوم با فاصله خط سوم"
```

#### Bidirectional Digit Script Converter
Convert all numbers in a given raw block of text to Persian or English digits:
```python
import parsikit

text = "شماره تماس ما: 09123456789"
print(parsikit.convert_numbers(text, to="persian"))
# Output: "شماره تماس ما: ۰۹۱۲۳۴۵۶۷۸۹"

print(parsikit.convert_numbers("کد امنیتی: ۱۲۵۰۰", to="english"))
# Output: "کد امنیتی: 12500"
```

---

### 4. Smart Classifiers & Sensitive Data Masking
Implement smart validation pipelines and protect sensitive user logs or profiles from exposure.

#### Universal Input Identifier (`detect`)
Automatically parses any string input to categorize its semantic data type:
```python
import parsikit

print(parsikit.detect("09123456789")) # "mobile_number"
print(parsikit.detect("7730123452"))  # "national_code"
print(parsikit.detect("ali@example.com")) # "email"
print(parsikit.detect("192.168.1.1")) # "ip"
print(parsikit.detect("https://google.com")) # "url"
print(parsikit.detect("some general phrase")) # None
```

#### Sensitive Data Masking Utilities
Perfect for admin panel fields, user profile previews, and secure database logging:
```python
import parsikit

# Mask Mobile Numbers
print(parsikit.mask_mobile("09123456789"))
# Output: "0912***6789"

# Mask Bank Cards (preserves standard formatted chunks)
print(parsikit.mask_card("6037991122334455", mask_char="X"))
# Output: "6037-99XX-XXXX-4455"

# Mask National Codes (preserves formatted XXX-XXXXXX-X layout)
print(parsikit.mask_national_code("7730123452"))
# Output: "773-****45-2"

# Mask Email usernames proportionally
print(parsikit.mask_email("kamrani.exe@gmail.com"))
# Output: "ka******e@gmail.com"
```

---

### 5. Calendar conversions, Fintech, Reshapers & Old Modules
All standard tools from previous versions remain completely supported.

#### Astronomical Shamsi Calendar & Time Humanizer
```python
import parsikit
import datetime

# Gregorian to Jalali (Cached for performance)
jy, jm, jd = parsikit.gregorian_to_jalali(2026, 7, 5)
print(parsikit.format_jalali(jy, jm, jd, "YYYY-MM-DD"))
# Output: "1405-04-14"

# Check leap year (Precise astronomical cycle)
print(parsikit.is_jalali_leap(1403)) # True

# Relative Time Humanizer
posted_at = datetime.datetime.now() - datetime.timedelta(hours=3)
print(parsikit.humanize_relative_time(posted_at))
# Output: "۳ ساعت پیش"
```

#### Graphical Reshaper (Diacritics-Aware)
```python
import parsikit

# Reshapes connected text for canvas engines with poor RTL support (OpenCV, Pygame, Pillow)
shaped = parsikit.reshape_for_graphics("عَلِیّ", reverse=False)
print(shaped) # "ﻋَﻠِﻲّ"
```

#### Cross-Framework GUI Binding (Tkinter / PySide / PyQt)
```python
import parsikit
from PySide6.QtWidgets import QLineEdit, QApplication

app = QApplication([])
card_input = QLineEdit()

# Auto-formats card digits reactive-style as "XXXX-XXXX-XXXX-XXXX" as the user types
parsikit.bind_persian_input(card_input, "card_number")

card_input.show()
app.exec()
```

---

## 🧪 Running Tests

A comprehensive, bug-free unit test suite is included in the project root to guarantee full structural compliance:

```bash
python -m unittest test.py
# or
python test.py
```

---

## 👨‍💻 Author

**Ali Kamrani**

- GitHub: [@MRThugh](https://github.com/MRThugh)
- Email: kamrani.exe@gmail.com

---

## 📄 License

This project is licensed under the **MIT License**. Feel free to use, modify, and distribute it in your commercial or open-source projects.

---

**ParsiKit** — Making Persian software development cleaner and more professional. 🚀