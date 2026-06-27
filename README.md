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

**A comprehensive, pure Python library for Persian text processing, validation, financial calculations, and graphical text reshaping.**

</div>

---

## 📖 Overview

**ParsiKit** (imported as `parsikit`) is a lightweight, zero-dependency, high-performance Python library designed to solve real-world Persian language challenges in software development.

Whether you need to normalize text, validate Iranian national IDs and bank accounts, convert numbers to words, calculate loan installments, or properly render Persian text in graphics engines (Pillow, Pygame, etc.), ParsiKit provides clean, fast, and reliable solutions using optimized translation tables and standard algorithms.

**Version:** 2.1.0

---

## ✨ Features

- **✍️ Text Normalization**
  - Arabic to Persian character conversion (ي → ی, ك → ک, etc.)
  - Smart Zero-Width Non-Joiner (نیم‌فاصله) correction
  - Diacritics (حرکات) removal
  - English keyboard layout correction (e.g. `sghl` → `سلام`)

- **🔢 Number Utilities**
  - Digit conversion (English ↔ Persian ↔ Arabic-Indic)
  - Number to Persian words (up to quadrillions)

- **💰 Currency & Financial Tools**
  - Currency formatting with thousands separators
  - Rial ↔ Toman conversion
  - Convert amount to Persian words
  - VAT / Tax calculation
  - Loan monthly installment calculation (PMT)

- **🔐 Iranian Standards Validators**
  - National Code (کد ملی) validation + formatting
  - Mobile number validation + normalization
  - Bank Card validation (Luhn algorithm)
  - Sheba (IBAN) validation + formatting

- **🎨 Graphical Reshaping**
  - Persian text shaping for engines with weak RTL support
  - Proper letter connection and Lam-Alef ligatures
  - Bidirectional (RTL/LTR) block handling

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

### 1. Text Normalization

```python
from parsikit import standardize_persian, strip_diacritics, correct_keyboard_layout

text = "ي كافيه ك کتاب ها ميباشد سَلامٌ"
print(standardize_persian(text))
# Output: "ی کافیه ک کتاب‌ها میباشد سلام"

print(strip_diacritics("عَلِیّ"))
# Output: "علی"

print(correct_keyboard_layout("sghl dm"))
# Output: "سلام خوب"
```

### 2. Number & Words Conversion

```python
from parsikit import english_to_persian, persian_to_english, number_to_words

print(english_to_persian("Price: 12500"))
# Output: "Price: ۱۲۵۰۰"

print(number_to_words(1453200))
# Output: "یک میلیون و چهارصد و پنجاه و سه هزار و دویست"

print(number_to_words(-500))
# Output: "منفی پانصد"
```

### 3. Currency & Financial

```python
from parsikit import format_currency, format_currency_to_words, rial_to_toman, add_tax_and_toll, calculate_installments

print(format_currency(1500000, persian_digits=True))
# Output: "۱،۵۰۰،۰۰۰ تومان"

print(format_currency_to_words(1000000))
# Output: "یک میلیون تومان"

print(add_tax_and_toll(100000))                    # 10% VAT
# Output: 110000

# Loan installment example
print(calculate_installments(10000000, 18.0, 12))
# Output: 916799
```

### 4. Validators

```python
from parsikit import (
    is_valid_national_code, format_national_code,
    is_valid_mobile, normalize_mobile,
    is_valid_card_number, format_card_number,
    is_valid_sheba, format_sheba
)

print(is_valid_national_code("7730123452"))        # True
print(format_national_code("7730123452"))
# Output: "773-012345-2"

print(is_valid_mobile("+989123456789"))            # True
print(normalize_mobile("+989123456789", prefix="0"))
# Output: "09123456789"

print(is_valid_card_number("6037991122334455"))    # True
print(format_card_number("6037991122334455"))
# Output: "6037-9911-2233-4455"

print(is_valid_sheba("IR050170000000123456789012")) # True
```

### 5. Graphical Text Reshaping

```python
from parsikit import reshape_for_graphics

# For use in Pillow, Pygame, Matplotlib, etc.
print(reshape_for_graphics("سلام Hello جهان"))
# Output: something like "ﻡﻼﺳ Hello ﻥﺎﻬﺟ"
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
