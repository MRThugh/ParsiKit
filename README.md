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
[![Version](https://img.shields.io/badge/version-3.2.0-blue.svg)](https://github.com/MRThugh/ParsiKit)
[![Persian](https://img.shields.io/badge/lang-PERSIAN-green)](README-fa.md)
[![English](https://img.shields.io/badge/lang-English-blue)](README.md)

**A production-grade, highly performant, and pure Python software infrastructure for Persian text processing, validation, financial calculations, calendar conversions, and graphical text reshaping.**

</div>

---

## 📖 Overview

**ParsiKit** (imported as `parsikit`) is a robust, zero-dependency Python library designed as a full-scale infrastructure for Persian language applications.

With the release of **v3.2.0**, ParsiKit has evolved from a utility library to a **production-grade enterprise infrastructure**. It offers a unified procedural API alongside an elegant, rich **Object-Oriented Domain Model** engine. It natively integrates with modern validation engines (like **Pydantic v2** and **FastAPI**), provides thread-safe computation caching, allows global runtime configuration, and features a granular domain-specific exception system.

---

## 🚀 Key Architectural Pillars in v3.2.0

### 1. Unified Configuration & Thread-Safe Caching (`parsikit.config`, `parsikit.cache`)
* **Thread-Safe Caching**: Highly repetitive and CPU-bound operations (such as converting large digits to words or parsing database dates) are optimized with an internal thread-safe LRU-like cache.
* **Global Configurations**: Easily control default parameters like value-added tax rates, default currency units, or toggle caching on/off dynamically at runtime.

### 2. Custom Structured Exceptions (`parsikit.exceptions`)
Never worry about managing generic `ValueError` or `TypeError` crashes. ParsiKit 3.2.0 ships with a structured exception tree tailored to Iranian standards, making it perfect for Clean Architecture or DDD pipelines.

### 3. Object-Oriented Domain Models (`parsikit.models`)
Wrap raw strings in rich domain models like `PersianText`, `NationalCode`, `MobileNumber`, `FixedLine`, `BankCard`, `Sheba`, or `VehiclePlate`. These models validate inputs upon instantiation, extract rich metadata (like province/city of issue, operators, or bank details), and serialize cleanly.

### 4. String Emulation (Duck Typing) & Dictionary Serialization (New in v3.2.0!)
All domain models act exactly like read-only Python strings. You can run string methods, index, slice, check length, or compare them directly with native strings. Additionally, every model features a `.to_dict()` and `.dict()` method for instant JSON-ready serialization.

### 5. Native Pydantic v2 & FastAPI Integration (New in v3.2.0!)
Use ParsiKit models directly as fields inside Pydantic schemas or FastAPI query/body parameters. ParsiKit handles validation, error propagation, and JSON serialization natively with **zero** external library dependencies.

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

### 1. Text Normalization, Collation & Scrapers
```python
import parsikit

# Chained transformations using PersianText
text = parsikit.PersianText("ي كافيه ك کتاب ها ميباشد سَلامٌ")
print(text.standardize().beautify())
# Output: "ی کافیه ک کتاب‌ها میباشد سلام"

# Correct keyboard layout mistyping
layout_err = parsikit.PersianText("sghl dm")
print(layout_err.correct_layout())
# Output: "سلام خوب"

# Advanced Persian sorting (Alphabetically corrects: پ, ژ, گ, etc.)
unsorted_list = ["گوسفند", "پروانه", "سیب", "ژاله", "آسمان", "باد"]
print(parsikit.persian_sorted(unsorted_list))
# Output: ["آسمان", "باد", "پروانه", "ژاله", "سیب", "گوسفند"]

# Scrape and normalize valid entities from raw texts
raw_paragraph = "شماره همراه من ۰۹۱۲۳۴۵۶۷۸۹ و کد ملی من ۷۷۳۰۱۲۳۴۵۲ هست."
extracted_phones = parsikit.extract_mobiles(raw_paragraph)
extracted_ids = parsikit.extract_national_codes(raw_paragraph)
print(extracted_phones) # ["09123456789"]
print(extracted_ids)    # ["7730123452"]
```

### 2. Numerics, Word Scales & Converters
```python
import parsikit

# Textual numbers to integers (Supports Septillions)
text_num = parsikit.PersianText("سی و دو هزار و پانصد")
print(text_num.to_number())
# Output: 32500

# Convert numbers to Persian words
print(parsikit.number_to_words("10,000,000,000,000,000,000"))
# Output: "ده کوئینتیلیون"

# Convert English digits to Persian and vice-versa
print(parsikit.english_to_persian("Price: 12500")) # "Price: ۱۲۵۰۰"
print(parsikit.persian_to_english("۱۲۵۰۰"))        # "12500"
```

### 3. Financial, Loans & Tax Instruments
```python
import parsikit

# Formatted currency with thousands separator
print(parsikit.format_currency(1500000, persian_digits=True))
# Output: "۱،۵۰۰،۰۰۰ تومان"

# Translate currencies to verbal words
print(parsikit.format_currency_to_words(250000, currency="toman"))
# Output: "دویست و پنجاه هزار تومان"

# VAT Addition (Uses config.default_tax_rate if None)
print(parsikit.add_tax_and_toll(100000))
# Output: 110000 (Based on 10% default VAT)

# Loan monthly installment plan (Amortization formula)
installment = parsikit.calculate_installments("10,000,000", annual_interest_rate=18.0, months=12)
print(installment) # 916799
```

### 4. Identity, Telecom & Landline Utilities
```python
import parsikit

# National Code
nc = parsikit.NationalCode("0010123451")
print(nc.formatted) # "001-012345-1"
print(nc.location)  # {"province": "تهران", "city": "تهران مرکزی"}

# Mobile Numbers
mob = parsikit.MobileNumber("+98۹۱۲۳۴۵۶۷۸۹")
print(mob.to_national())      # "09123456789"
print(mob.to_international()) # "+989123456789"
print(mob.operator)          # "MCI"

# Landline / Fixed Telephone Numbers
land = parsikit.FixedLine("02188888888")
print(land.province)          # "تهران"
print(land.area_code)         # "021"
print(land.to_international()) # "+982188888888"

# Vehicle Plate Parser
plate = parsikit.VehiclePlate("۱۲ ب ۳۴۵ ایران ۶۸")
print(plate.province)         # "البرز"
print(plate.category)         # "شخصی"
print(plate.formatted)        # "۱۲ ب ۳۴۵ - ایران ۶۸"
```

### 5. Fintech & Billing Utilities
```python
import parsikit

# Detect bank details from Card numbers
card = parsikit.BankCard("6037991122334455")
print(card.bank) # {"name": "بانک ملی ایران", "code": "melli"}
print(card.formatted) # "6037-9911-2233-4455"

# Detect bank and extract Account Number from Sheba (IBAN)
sheba = parsikit.Sheba("IR050120000000123456789012")
print(sheba.bank)           # {"name": "بانک ملت", "code": "mellat"}
print(sheba.account_number) # "123456789012"

# Parse and validate Invoice/Utility bill IDs (Modulo 11 compliant)
bill_id, pay_id = "7748317800142", "1770160"
bill_details = parsikit.extract_bill_details(bill_id, pay_id)
print(bill_details)
# Output: {'is_valid': True, 'amount_rial': 17701000, 'amount_toman': 1770100, 'type': 'تلفن ثابت', 'type_code': '4'}
```

### 6. Astronomical Shamsi Calendar & Time Humanizer
```python
import parsikit
import datetime

# Gregorian to Jalali (Cached for performance)
jy, jm, jd = parsikit.gregorian_to_jalali(2026, 7, 5)
print(parsikit.format_jalali(jy, jm, jd, "YYYY-MM-DD"))
# Output: "1405-04-14"

# Check leap year (Precise astronomical cycle)
print(parsikit.is_jalali_leap(1403)) # True

# Get Persian month name
print(parsikit.get_jalali_month_name(4)) # "تیر"

# Relative Time Humanizer
posted_at = datetime.datetime.now() - datetime.timedelta(hours=3)
print(parsikit.humanize_relative_time(posted_at))
# Output: "۳ ساعت پیش"
```

### 7. Graphical Reshaper (Diacritics-Aware)
```python
import parsikit

# Reshapes connected text for canvas engines with poor RTL support (OpenCV, Pygame, Pillow)
# Keeps diacritics in physical place without interrupting Persian word flow
shaped = parsikit.reshape_for_graphics("عَلِیّ", reverse=False)
print(shaped) # "ﻋَﻠِﻲّ"

# Automatic paragraph wrapping into multi-line RTL blocks
paragraph = "سلام جهان این یک متن بسیار طولانی برای تست بسته بندی خودکار خطوط فارسی است"
wrapped_lines = parsikit.reshape_paragraph_for_graphics(paragraph, max_chars_per_line=20)
for line in wrapped_lines:
    print(line)
```

### 8. Cross-Framework GUI Binding (Tkinter / PySide / PyQt)
```python
# Real-time reactive formatting as the user types (preserving insertion cursors)
import parsikit
from PySide6.QtWidgets import QLineEdit, QApplication

app = QApplication([])
card_input = QLineEdit()

# Auto-formats card digits reactive-style as "XXXX-XXXX-XXXX-XXXX"
parsikit.bind_persian_input(card_input, "card_number")

card_input.show()
app.exec()
```

---

## 🧪 Running Tests

A comprehensive unit test suite is included in the project root to guarantee full structural compliance:

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
