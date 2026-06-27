<div align="center" dir="rtl">

# 🌟 کتابخانه ParsiKit 🌟
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

**یک کتابخانهٔ سبک، سریع و بدون وابستگی برای پردازش متن فارسی، اعتبارسنجی، محاسبات مالی و شکل‌دهی متن برای گرافیک.**

</div>

---

## 📖 معرفی

**ParsiKit** (قابل ایمپورت به صورت `parsikit`) یک کتابخانهٔ خالص پایتون است که مشکلات رایج کار با زبان فارسی در توسعهٔ نرم‌افزار را حل می‌کند.

چه نیاز به نرمال‌سازی متن، اعتبارسنجی کد ملی و شبا، تبدیل عدد به حروف، محاسبه قسط وام، یا نمایش صحیح متن فارسی در موتورهای گرافیکی (مانند Pillow، Pygame، Matplotlib و ...) داشته باشید، ParsiKit با عملکرد بالا و کد تمیز به شما کمک می‌کند.

**نسخه:** ۲.۱.۰

---

## ✨ امکانات

- **✍️ نرمال‌سازی متن**
  - تبدیل حروف عربی به فارسی (ي → ی، ك → ک و ...)
  - اصلاح هوشمند نیم‌فاصله (ZWNJ)
  - حذف حرکات (تشدید، فتحه، کسره و ...)
  - اصلاح صفحه‌کلید انگلیسی به فارسی (مثلاً `sghl` → `سلام`)

- **🔢 کار با اعداد**
  - تبدیل اعداد انگلیسی، فارسی و عربی به یکدیگر
  - تبدیل عدد به حروف فارسی (تا کوآدریلیون)

- **💰 امور مالی و پولی**
  - فرمت کردن اعداد با جداکننده هزارگان
  - تبدیل ریال به تومان و بالعکس
  - تبدیل مبلغ به حروف فارسی
  - محاسبه مالیات بر ارزش افزوده (VAT)
  - محاسبه قسط ماهانه وام

- **🔐 اعتبارسنجی استانداردهای ایرانی**
  - اعتبارسنجی و فرمت کد ملی
  - اعتبارسنجی و نرمال‌سازی شماره موبایل
  - اعتبارسنجی شماره کارت بانکی (الگوریتم Luhn)
  - اعتبارسنجی و فرمت شبا (IBAN)

- **🎨 شکل‌دهی متن برای گرافیک**
  - اتصال صحیح حروف فارسی (Shaping)
  - پشتیبانی از ligature لام و الف
  - مدیریت بلوک‌های راست به چپ و چپ به راست

همه عملیات با **عملکرد O(n)** و استفاده از جدول ترجمه بهینه انجام می‌شوند.

---

## ⚙️ نصب

```bash
git clone https://github.com/MRThugh/ParsiKit.git
cd ParsiKit
pip install .
```
**یا**

```bash
pip install parsikit
```
**نیازمند:** Python 3.10 به بالا

---

## 🚀 نحوه استفاده

### ۱. نرمال‌سازی متن

```python
from parsikit import standardize_persian, strip_diacritics, correct_keyboard_layout

text = "ي كافيه ك کتاب ها ميباشد سَلامٌ"
print(standardize_persian(text))
# خروجی: «ی کافیه ک کتاب‌ها میباشد سلام»

print(strip_diacritics("عَلِیّ"))
# خروجی: «علی»

print(correct_keyboard_layout("sghl dm"))
# خروجی: «سلام خوب»
```

### ۲. تبدیل اعداد و نوشتن به حروف

```python
from parsikit import english_to_persian, persian_to_english, number_to_words

print(english_to_persian("Price: 12500"))
# خروجی: «Price: ۱۲۵۰۰»

print(number_to_words(1453200))
# خروجی: «یک میلیون و چهارصد و پنجاه و سه هزار و دویست»
```

### ۳. امور مالی

```python
from parsikit import format_currency, format_currency_to_words, add_tax_and_toll, calculate_installments

print(format_currency(1500000, persian_digits=True))
# خروجی: «۱،۵۰۰،۰۰۰ تومان»

print(format_currency_to_words(1000000))
# خروجی: «یک میلیون تومان»

print(add_tax_and_toll(100000))        # مالیات ۱۰٪
# خروجی: 110000

# مثال محاسبه قسط وام
print(calculate_installments(10000000, 18.0, 12))
# خروجی: 916799
```

### ۴. اعتبارسنجی‌ها

```python
from parsikit import (
    is_valid_national_code, format_national_code,
    is_valid_mobile, normalize_mobile,
    is_valid_card_number, format_card_number,
    is_valid_sheba, format_sheba
)

print(is_valid_national_code("7730123452"))   # True
print(format_national_code("7730123452"))
# خروجی: «773-012345-2»

print(is_valid_mobile("+989123456789"))       # True

print(is_valid_card_number("6037991122334455")) # True
```

### ۵. شکل‌دهی متن برای گرافیک

```python
from parsikit import reshape_for_graphics

text = reshape_for_graphics("سلام Hello جهان")
print(text)
# مناسب برای Pillow، Pygame و موتورهایی که پشتیبانی RTL ضعیفی دارند
```

---

## 🧪 اجرای تست‌ها

```bash
python test.py
```

---

## 👨‍💻 نویسنده

**علی کامرانی**

- GitHub: [@MRThugh](https://github.com/MRThugh)
- ایمیل: kamrani.exe@gmail.com

---

## 📄 مجوز

این پروژه تحت مجوز **MIT** منتشر شده است. می‌توانید آزادانه از آن استفاده، تغییر دهید و در پروژه‌های خود به کار ببرید.

---

**ParsiKit** — توسعه نرم‌افزار فارسی را راحت‌تر و حرفه‌ای‌تر می‌کند. 🚀.
