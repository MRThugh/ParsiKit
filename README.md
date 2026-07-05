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
[![Persian](https://img.shields.io/badge/lang-PERSIAN-green)](README-fa.md)
[![English](https://img.shields.io/badge/lang-English-blue)](README.md)

**A comprehensive, pure Python library for Persian text processing, validation, financial calculations, calendar conversions, and graphical text reshaping.**

</div>

---

## 📖 Overview

**ParsiKit** (imported as `parsikit`) is a lightweight, zero-dependency, high-performance Python library designed to solve real-world Persian language challenges in software development.

Whether you need to normalize text, validate Iranian national IDs, format bank cards, detect bank issuers from card/Sheba numbers, analyze utility bills, parse vehicle license plates, convert numbers to words up to Septillions, calculate loan installments, or properly render Persian text with diacritics in graphics engines (Pillow, Pygame, etc.), ParsiKit provides clean, fast, and reliable solutions using optimized translation tables, standard algorithms, and zero-dependency GUI helpers.

**Version:** 2.8.0

---

## ✨ Features

- **✍️ Text Normalization & Typographic Beautifier**
  - Arabic to Persian character conversion (`ي` → `ی`, `ك` → `ک`, etc.)
  - Smart Zero-Width Non-Joiner (نیم‌فاصله) correction for verbs and suffixes
  - Diacritics (حرکات) removal
  - English keyboard layout correction (e.g. `sghl` → `سلام`)
  - **Typographic spacing beautifier** (`beautify_persian_spacing`): auto-corrects spacings around punctuation, removes spaces inside parentheses/brackets, and dynamically converts typed layout commas `,` and semicolons `;` to Persian equivalents when surrounded by Persian characters.
  - Correct Persian sorting/collation (`persian_sort_key` and `persian_sorted`): standardizes alphabetical sorting for Persian-specific characters like `پ`, `ژ`, `گ` which are natively sorted incorrectly in standard Python.

- **🔢 Number Utilities**
  - Digit conversion (English ↔ Persian ↔ Arabic-Indic)
  - Number to Persian words (supports exceptionally large numbers up to Septillions ($10^{24}$)) with auto-formatting character cleanup (commas, spaces).

- **💰 Currency & Financial Tools**
  - Currency formatting with thousands separators and Persian digit support
  - Rial ↔ Toman conversion
  - Convert amount to Persian words with native currency labels
  - VAT / Tax calculation (including 10% VAT default calculator)
  - Loan monthly installment calculation (amortization formulas)

- **🔐 Iranian Standards Validators & Formatter**
  - National Code (کد ملی) validation (with omitted leading zeros padding) + formatting
  - Mobile number validation + normalization with extended international prefixes (`0098`, `+98`, empty bare)
  - Bank Card validation (Luhn algorithm) + 4-chunk group formatting
  - Sheba (IBAN) validation + spacing block formatting (immune to custom delimiters)
  - Corporate/Legal Entity National ID (شناسه ملی حقوقی) validator
  - **Structural 10-digit Postal Code validation**: checks OCR guidelines where first 5 digits cannot contain `0` or `2`, and formats them as `XXXXX-XXXXX`.
  - **Iranian National Vehicle License Plate (پلاک ملی) Parser & Validator**: parses plate parts, determines car categories (Personal, Taxi, Government, Military, etc.), maps the province code directly to the issuing Persian province name, and formats them.

- **🏦 Fintech & Billing Utilities**
  - **Bank Issuer Detection**: dynamically detects bank details (Persian name and English slug) from card numbers/BIN prefixes or Sheba/IBAN codes.
  - **Invoice & Bill Payments Validator**: validates Bill ID and Payment ID using standard Modulo-11 check digit rules and extracts payment amounts (in Rials and Tomans) and bill classifications (Water, Electricity, Gas, Telephone, etc.).

- **📅 Astronomical Calendar Converter**
  - High-precision, zero-dependency, arithmetic-based calendar converters between Gregorian and Jalali (Shamsi) and a pattern-based date formatter (`YYYY/MM/DD`).

- **🎨 Graphical Reshaping**
  - Persian text shaping for engines with weak RTL support (Pillow, Pygame, OpenCV, Godot, Matplotlib, arcade)
  - **Diacritics-Aware Shaping**: ignores diacritics/Harakat (Fatha, Kasra, Tashdeed, Sukuun, etc.) when calculating character-level chasis connectivity so they don't break Persian word flow, whilst preserving them in the exact physical location.
  - Auto-wrapping multiline paragraph wrapper (`reshape_paragraph_for_graphics`) to dynamically break down long sentences for canvas boundaries.

- **🖥️ Cross-Framework GUI Binding Helper**
  - Real-time event hooks (`bind_persian_input`) for **Tkinter (Entry)**, **CustomTkinter (CTkEntry)**, and **PyQt/PySide (QLineEdit)** to format texts, credit cards, national codes, postal codes, and shebas dynamically *as the user types* without messing up cursor positions.

All operations are optimized for **O(n)** performance.

---

## ⚙️ Installation

```bash
git clone https://github.com/MRThugh/ParsiKit.git
cd ParsiKit
pip install .
```
**Or**

```bash
pip install parsikit
```

**Requires Python 3.10+**

---

## 🚀 Quick Start & Usage

### 1. Text Normalization, Collation & Beautifier

```python
import parsikit

# Standardization and ZWNJ formatting
text = "ي كافيه ك کتاب ها ميباشد سَلامٌ"
print(parsikit.standardize_persian(text))
# Output: "ی کافیه ک کتاب‌ها میباشد سلام"

# Correct mistyped English layout text
print(parsikit.correct_keyboard_layout("sghl dm"))
# Output: "سلام خوب"

# Spacing and layout typographical beautifier
dirty_type = "سلام , چطوری ؟ من خوبم.سیب,گلابی,پرتقال.امروز( شنبه ) فردا(یکشنبه) است."
print(parsikit.beautify_persian_spacing(dirty_type))
# Output: "سلام، چطوری؟ من خوبم. سیب، گلابی، پرتقال. امروز (شنبه) فردا (یکشنبه) است."

# Advanced alphabetical sorting (Correcting default Python sorting order)
items = ["گوسفند", "پروانه", "سیب", "ژاله", "آسمان", "باد"]
print(parsikit.persian_sorted(items))
# Output: ["آسمان", "باد", "پروانه", "ژاله", "سیب", "گوسفند"]
```

### 2. Number & Words Conversion

```python
import parsikit

# Convert digits
print(parsikit.english_to_persian("Price: 12500"))
# Output: "Price: ۱۲۵۰۰"

# Large digits to verbal words
print(parsikit.number_to_words("10,000,000,000,000,000,000"))
# Output: "ده کوئینتیلیون"
```

### 3. Currency, Loans & VAT Calculations

```python
import parsikit

# Format with thousands separators
print(parsikit.format_currency(1500000, persian_digits=True))
# Output: "۱،۵۰۰،۰۰۰ تومان"

# VAT Addition (Default is 10%)
print(parsikit.add_tax_and_toll(100000))
# Output: 110000

# Loan installment planning (Amortization)
print(parsikit.calculate_installments("10,000,000", annual_interest_rate=18.0, months=12))
# Output: 916799
```

### 4. Identity & Telecom Validators

```python
import parsikit

# National Code validation (auto-pads omitted leading zeros)
print(parsikit.is_valid_national_code("773012345"))  # True (padded to 0773012345)
print(parsikit.format_national_code("0773012345"))
# Output: "077-301234-5"

# Corporate ID validation
print(parsikit.is_valid_corporate_id("14003632892")) # True

# Mobile verification & operator detection
print(parsikit.is_valid_mobile("+989123456789"))     # True
print(parsikit.detect_mobile_operator("09121112233"))
# Output: "همراه اول (MCI)"
```

### 5. Fintech & Billing Utilities

```python
import parsikit

# Bank Card Issuer detection (BIN/Prefix or full card)
bank = parsikit.detect_bank_from_card("6037991122334455")
print(bank)
# Output: {'name': 'بانک ملی ایران', 'code': 'melli'}

# Sheba Issuer detection
bank_sheba = parsikit.detect_bank_from_sheba("IR050120000000123456789012")
print(bank_sheba)
# Output: {'name': 'بانک ملت', 'code': 'mellat'}

# Utility bill payments validation & extraction (Modulo-11 compliance)
bill_id = "7748317800142"
pay_id = "1770160"
print(parsikit.is_valid_bill_and_payment(bill_id, pay_id)) # True

details = parsikit.extract_bill_details(bill_id, pay_id)
print(details)
# Output: {'is_valid': True, 'amount_rial': 17701000, 'amount_toman': 1770100, 'type': 'تلفن ثابت', 'type_code': '4'}
```

### 6. Postal Code & Vehicle License Plates

```python
import parsikit

# Structural Postal Code checks
print(parsikit.is_valid_postal_code("1453902410"))  # True
print(parsikit.is_valid_postal_code("1453202410"))  # False (First 5 digits can't contain 0 or 2)
print(parsikit.format_postal_code("1453902410"))
# Output: "14539-02410"

# Iranian National Vehicle License Plate parser & validator
plate = "۱۲ ب ۳۴۵ ایران ۶۸"
print(parsikit.is_valid_plate(plate))                # True

parsed_plate = parsikit.parse_plate(plate)
print(parsed_plate)
# Output: {'part1': '۱۲', 'letter': 'ب', 'part2': '۳۴۵', 'province_code': '۶۸', 'province': 'البرز', 'category': 'شخصی'}

print(parsikit.format_plate(plate, format_type="readable"))
# Output: "۱۲ ب ۳۴۵ - ایران ۶۸"
```

### 7. Astronomical Shamsi Calendar Converter

```python
import parsikit

# Gregorian (2026-07-05) to Jalali
jy, jm, jd = parsikit.gregorian_to_jalali(2026, 7, 5)
print(parsikit.format_jalali(jy, jm, jd, "YYYY/MM/DD"))
# Output: "1405/04/14"

# Jalali back to Gregorian
gy, gm, gd = parsikit.jalali_to_gregorian(1405, 4, 14)
print(f"{gy}-{gm}-{gd}")
# Output: "2026-7-5"
```

### 8. Graphical Reshaper (Diacritics-Aware)

```python
import parsikit

# Reshapes text with diacritics/Harakat without losing connectivity (for Pillow, Pygame, arcade)
print(parsikit.reshape_for_graphics("عَلِیّ", reverse=False))
# Output: "ﻋَﻠِﻲّ" (Correct connected form with Harakat preserved)

# Long Paragraph automatic wrapping (returns a list of lines shaped for RTL rendering)
paragraph = "سلام جهان این یک متن بسیار طولانی برای تست بسته بندی خودکار خطوط فارسی است"
wrapped_lines = parsikit.reshape_paragraph_for_graphics(paragraph, max_chars_per_line=20)
for line in wrapped_lines:
    print(line)
```

### 9. Cross-Framework GUI Binding (Tkinter/PySide/PyQt)

```python
# Bind to QLineEdit (PySide/PyQt) or Entry (Tkinter) for real-time formatting
import parsikit
from PySide6.QtWidgets import QLineEdit, QApplication

app = QApplication([])
card_input = QLineEdit()

# Dynamically formats card number as the user types without disrupting cursor position
parsikit.bind_persian_input(card_input, "card_number")

card_input.show()
app.exec()
```

---

## 🧪 Running Tests

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

This project is licensed under the **MIT License**. Feel free to use, modify, and distribute it in your projects.

---

**ParsiKit** — Making Persian software development cleaner and more professional. 🚀