<div align="center">

# 🌟 ParsiKit AstraNest Explorer 🌟

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Author](https://img.shields.io/badge/author-Ali%20Kamrani-purple.svg)](https://github.com/MRThugh)

**A pure, high-performance Python library for Persian data formatting, text normalization, and currency conversion.**

</div>

---

## 📖 Overview

**ParsiKit AstraNest Explorer** (imported as `parsikit`) is a lightweight, dependency-free toolkit designed to handle the nuances of the Persian language in software development. Whether you need to normalize Arabic characters to Persian, correct zero-width non-joiners (نیم‌فاصله), convert digits, or format monetary values (Rial/Toman), ParsiKit handles it with $O(n)$ performance using optimized translation tables.

---

## ✨ Features

- ✍️ **Text Normalization:** Converts Arabic characters (ي, ك, etc.) to their Persian equivalents (ی, ک).
- 🧩 **Smart ZWNJ (نیم‌فاصله) Correction:** Automatically fixes spacing for common Persian prefixes (می, نمی) and suffixes (ها, های).
- 🔢 **Digit Conversion:** Seamlessly translate between English (ASCII), Persian, and Arabic-Indic digits.
- 💰 **Currency Formatting:** Format large numbers into human-readable currency strings (Toman/Rial).
- 🧮 **Currency Conversion:** Safely convert Iranian Rials to Tomans using integer division ($T = \lfloor \frac{R}{10} \rfloor$).

---

## ⚙️ Installation

Since this is a standard Python package, you can install it directly via `pip` from the source directory. ParsiKit requires **Python 3.10+**.

```bash
# Clone the repository
git clone https://github.com/MRThugh/ParsiKit.git

# Navigate to the project directory
cd ParsiKit

# Install the package
pip install .
```

---

## 🚀 Quick Start & Usage

### 1. Text Normalization (`parsikit.text`)
Clean up user input by fixing Arabic characters, applying ZWNJs correctly, and removing redundant whitespaces.

```python
from parsikit import standardize_persian

# Arabic characters and bad spacing
raw_text = "ي كتاب   مي خوانم"
clean_text = standardize_persian(raw_text)

print(clean_text) 
# Output: 'ی کتاب می‌خوانم'
```

### 2. Number Conversion (`parsikit.number`)
Convert numeric strings between English and Persian scripts safely. Excellent for sanitizing database inputs or preparing data for UI display.

```python
from parsikit import english_to_persian, persian_to_english

# English/Arabic to Persian
print(english_to_persian("Order 123 - ١٢٣")) 
# Output: 'Order ۱۲۳ - ۱۲۳'

# Persian/Arabic to English (ASCII)
print(persian_to_english("قیمت: ۱۲۳۴")) 
# Output: 'قیمت: 1234'
```

### 3. Currency Handling (`parsikit.currency`)
Format raw integers or Persian string numbers into beautifully formatted monetary values. Convert Rial to Toman mathematically ($Toman = Rial \div 10$).

```python
from parsikit import format_currency, rial_to_toman

# Basic Toman formatting
print(format_currency(1500000))
# Output: '1,500,000 تومان'

# Persian digits output
print(format_currency("۱۵۰۰۰۰", persian_digits=True))
# Output: '۱۵۰،۰۰۰ تومان'

# Rial to Toman conversion
rial_amount = 5000000
toman_amount = rial_to_toman(rial_amount)
print(format_currency(toman_amount, "toman", persian_digits=True))
# Output: '۵۰۰،۰۰۰ تومان'
```

---

## 🧪 Running Tests

The library comes with a comprehensive test suite to ensure reliability across all modules.

You can run the tests using `unittest`:
```bash
python -m unittest discover -s tests
```
Or using `pytest`:
```bash
python -m pytest test.py
```

---

## 👨‍💻 Author

**Ali Kamrani**
- GitHub: [@MRThugh](https://github.com/MRThugh)
- Email: kamrani.exe@gmail.com

## 📄 License

This project is licensed under the **MIT License**. Feel free to use, modify, and distribute it in your own projects.
