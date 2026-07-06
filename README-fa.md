<div align="center">

# 🌟 کتابخانه ParsiKit (پارسی‌کیت) 🌟
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

**یک زیرساخت نرم‌افزاری بومی، سبک و بدون وابستگی برای پردازش متن، اعتبارسنجی داده‌ها، محاسبات مالی، تقویم جلالی و بهبود گرافیک متون فارسی در پایتون.**

</div>

---

## 📖 معرفی کوتاه

**پارسی‌کیت** (که به صورت `parsikit` ایمپورت می‌شود) یک ابزار سبک، سریع و کاملاً بدون وابستگی (Zero-Dependency) است که با هدف حل چالش‌های روزمره زبان فارسی در توسعه نرم‌افزار طراحی شده است.

در **نسخه 3.2.0**، پارسی‌کیت از یک کیتِ کاربردیِ ساده به یک **فریم‌ورک زیرساختی آماده برای محیط‌های تجاری** ارتقا یافته است. این نسخه علاوه بر ارائه توابع مستقیم (Procedural API)، یک سیستم **مدل‌های دامنه شیءگرا (OOP Domain Models)** ارائه می‌دهد که به صورت بومی با ابزارهایی مثل **Pydantic v2** و **FastAPI** هماهنگ است، از کش چندنخی (Thread-safe) برای پردازش‌های سنگین استفاده می‌کند، اجازه پیکربندی سراسری در زمان اجرا را می‌دهد و خطاهای ساختاریافته اختصاصی صادر می‌کند.

---

## 🚀 ویژگی‌های کلیدی در نسخه 3.2.0

### ۱. مدیریت تنظیمات سراسری و کش محاسباتی چندنخی (`parsikit.config`, `parsikit.cache`)
* **کش هوشمند و چندنخی**: محاسبات سنگین (مانند تبدیل تاریخ‌ها در خروجی دیتابیس یا تبدیل ابعاد بزرگ اعداد به حروف فارسی) با یک مکانیزم کش چندنخی بهینه‌سازی شده‌اند تا سرعت اجرای پایپ‌لاین‌ها در وب‌سرویس‌ها به حداکثر برسد.
* **کانفیگ متمرکز**: تغییر پارامترهای پیش‌فرض سیستم (مانند تغییر نرخ مالیات بر ارزش افزوده یا نوع ارز پیش‌فرض سیستم) در هر زمان از اجرای برنامه ممکن است.

### ۲. سیستم خطاهای ساختاریافته اختصاصی (`parsikit.exceptions`)
دیگر نیازی نیست خطاهای مبهم پایتون مانند `ValueError` را مدیریت کنید. تمام فرآیندهای اعتبارسنجی پارسی‌کیت خطاهای اختصاصی مرتبط با دامنه خود (مانند `InvalidNationalCodeError` یا `InvalidShebaError`) صادر می‌کنند تا مدیریت خطاها در معماری‌های تمیز کاملاً ایزوله باشد.

### ۳. مدل‌های دامنه شیءگرا و غنی (`parsikit.models`)
داده‌های خام را در قالب کلاس‌های هوشمندی مثل `PersianText` ،`NationalCode` ،`MobileNumber` ،`FixedLine` ،`BankCard` ،`Sheba` و `VehiclePlate` کپسوله‌سازی کنید. این مدل‌ها به محض ساخته شدن داده را بررسی کرده، متادیتای آن را استخراج می‌کنند و خروجی مرتب‌شده تحویل می‌دهند.

### ۴. شبیه‌سازی کاراکترها و خروجی دیکشنری (جدید در نسخه 3.2.0!)
تمام مدل‌های شیءگرای پارسی‌کیت دقیقاً رفتاری مشابه با رشته‌های پایتون (String Emulation) دارند. می‌توانید طول آن‌ها را با `len()` بگیرید، روی آن‌ها قطعه‌بندی (Slicing) انجام دهید یا آن‌ها را مستقیماً با یک رشته معمولی مقایسه کنید. همچنین متدهای `.to_dict()` و `.dict()` برای خروجی‌های JSON سریع فراهم شده است.

### ۵. ادغام بومی با Pydantic v2 و FastAPI (جدید در نسخه 3.2.0!)
کلاس‌های پارسی‌کیت را مستقیماً به عنوان نوع فیلد (Type Hint) در پایدنتیک بنویسید. پارسی‌کیت بدون نیاز به نصب اجباری هیچ لایبرری خارجی، فرآیند راستی‌آزمایی، لود داده‌ها و سریالایز خودکار در خروجی‌های FastAPI را انجام می‌دهد.

---

## ⚙️ روش نصب

```bash
pip install parsikit
```

**نیازمند پایتون ۳.۱۰ به بالا**

---

## 🔧 تنظیمات و مدیریت خطاهای سیستم

### ۱. پیکربندی سراسری ابزارها
```python
import parsikit

# تغییر نرخ مالیات بر ارزش افزوده در کل سیستم (پیش‌فرض: 0.10)
parsikit.config.default_tax_rate = 0.09

# تغییر واحد پولی پیش‌فرض محاسبات (پیش‌فرض: "toman")
parsikit.config.default_currency = "rial"

# فعال/غیرفعال‌سازی کش هوشمند چندنخی
parsikit.config.enable_cache = True
```

### ۲. سلسله‌مراتب خطاها
تمامی استثناهای اختصاصی فریم‌ورک از `parsikit.exceptions.ValidationError` ارث‌بری می‌کنند:
```python
import parsikit

try:
    card = parsikit.BankCard("شماره-کارت-نامعتبر")
except parsikit.InvalidCardNumberError as e:
    print(f"خطای پردازش کارت بانکی: {e}")
except parsikit.ValidationError as e:
    print(f"خطای اعتبارسنجی عمومی پارسی‌کیت: {e}")
```

---

## 🦄 ادغام بومی با Pydantic v2 و FastAPI

مدل‌های شیءگرای پارسی‌کیت را مستقیماً در کلاس‌های پایدنتیک و کدهای FastAPI استفاده کنید. این ابزارها به صورت خودکار داده‌های خام ورودی کاربر را اعتبارسنجی و تمیز می‌کنند:

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
    # داده‌ها قبل از ورود به این متد کاملاً اعتبارسنجی و مرتب شده‌اند!
    print(user.fullname.standardize())       # تبدیل حروف عربی و اعمال نیم‌فاصله
    print(user.national_id.location)         # مشخصات محل صدور: {"province": "تهران", "city": "تهران مرکزی"}
    print(user.phone.to_international())     # فرمت بین‌المللی: "+989123456789"
    
    # خروجی دیکشنری تمیز برای ذخیره در پایگاه داده
    return {
        "status": "success",
        "data": {
            "national_id": user.national_id.to_dict(),
            "card_bank": user.card.bank
        }
    }
```

---

## 🚀 راهنمای سریع و کدهای نمونه

### ۱. نرمال‌سازی متن، اصلاح فاصله‌ها و استخراج اطلاعات
```python
import parsikit

# اعمال تغییرات زنجیره‌ای با استفاده از کلاس متن فارسی
text = parsikit.PersianText("ي كافيه ك کتاب ها ميباشد سَلامٌ")
print(text.standardize().beautify())
# خروجی: "ی کافیه ک کتاب‌ها میباشد سلام"

# اصلاح کلماتی که با کیبورد انگلیسی تایپ شده‌اند
layout_err = parsikit.PersianText("sghl dm")
print(layout_err.correct_layout())
# خروجی: "سلام خوب"

# مرتب‌سازی الفبایی فارسی (اصلاح نادرستی پیش‌فرض پایتون در چینش حروف گ، ژ، پ و...)
items = ["گوسفند", "پروانه", "سیب", "ژاله", "آسمان", "باد"]
print(parsikit.persian_sorted(items))
# خروجی: ["آسمان", "باد", "پروانه", "ژاله", "سیب", "گوسفند"]

# استخراج کدهای ملی و شماره‌های موبایل واقعی از داخل متن‌های خام
raw_paragraph = "شماره همراه من ۰۹۱۲۳۴۵۶۷۸۹ و کد ملی من ۷۷۳۰۱۲۳۴۵۲ هست."
print(parsikit.extract_mobiles(raw_paragraph))       # ["09123456789"]
print(parsikit.extract_national_codes(raw_paragraph)) # ["7730123452"]
```

### ۲. تبدیل کلمات به عدد و عدد به حروف
```python
import parsikit

# تبدیل متن فارسی عددی به عدد صحیح (پشتیبانی تا عدد سپتیلیون)
text_num = parsikit.PersianText("سی و دو هزار و پانصد")
print(text_num.to_number())
# خروجی: 32500

# تبدیل عدد بزرگ به حروف فارسی
print(parsikit.number_to_words("10,000,000,000,000,000,000"))
# خروجی: "ده کوئینتیلیون"

# تبدیل انگلیسی <-> فارسی اعداد درون رشته‌ها
print(parsikit.english_to_persian("Price: 12500")) # "Price: ۱۲۵۰۰"
print(parsikit.persian_to_english("۱۲۵۰۰"))        # "12500"
```

### ۳. محاسبات مالی، اقساط وام و مالیات
```python
import parsikit

# فرمت دهی پولی با جداکننده سه رقمی و اعداد فارسی
print(parsikit.format_currency(1500000, persian_digits=True))
# خروجی: "۱،۵۰۰،۰۰۰ تومان"

# تبدیل مبالغ پولی به حروف فارسی با برچسب واحد پول
print(parsikit.format_currency_to_words(250000, currency="toman"))
# خروجی: "دویست و پنجاه هزار تومان"

# محاسبه خودکار مالیات بر ارزش افزوده (با امکان تغییر نرخ پیش‌فرض در لایه پیکربندی)
print(parsikit.add_tax_and_toll(100000))
# خروجی: 110000

# فرمول محاسبه دقیق اقساط ماهیانه وام بانکی
installment = parsikit.calculate_installments("10,000,000", annual_interest_rate=18.0, months=12)
print(installment) # 916799
```

### ۴. کد ملی، شماره‌های موبایل و تلفن ثابت
```python
import parsikit

# کلاس تخصصی کد ملی
nc = parsikit.NationalCode("0010123451")
print(nc.formatted) # "001-012345-1"
print(nc.location)  # {"province": "تهران", "city": "تهران مرکزی"}

# کلاس تخصصی شماره موبایل
mob = parsikit.MobileNumber("+98۹۱۲۳۴۵۶۷۸۹")
print(mob.to_national())      # "09123456789"
print(mob.to_international()) # "+989123456789"
print(mob.operator)           # "MCI"

# کلاس تخصصی تلفن‌های ثابت (اعتبارسنجی و موقعیت‌یابی هوشمند پیش‌شماره‌ها)
land = parsikit.FixedLine("02188888888")
print(land.province)          # "تهران"
print(land.area_code)         # "021"
print(land.to_international()) # "+982188888888"

# پارسر هوشمند پلاک ملی خودرو
plate = parsikit.VehiclePlate("۱۲ ب ۳۴۵ ایران ۶۸")
print(plate.province)         # "البرز"
print(plate.category)         # "شخصی"
print(plate.formatted)        # "۱۲ ب ۳۴۵ - ایران ۶۸"
```

### ۵. فین‌تک، کارت‌های بانکی، شبا و قبوض خدماتی
```python
import parsikit

# راستی‌آزمایی و واکشی بانک صادرکننده کارت شتاب
card = parsikit.BankCard("6037991122334455")
print(card.bank)      # {"name": "بانک ملی ایران", "code": "melli"}
print(card.formatted) # "6037-9911-2233-4455"

# راستی‌آزمایی شبا و استخراج شماره حساب منحصربه‌فرد بانکی
sheba = parsikit.Sheba("IR050120000000123456789012")
print(sheba.bank)           # {"name": "بانک ملت", "code": "mellat"}
print(sheba.account_number) # "123456789012"

# راستی‌آزمایی و تفکیک جزئیات کامل قبوض بر اساس الگوریتم ماژول ۱۱
bill_id = "7748317800142"
pay_id = "1770160"
details = parsikit.extract_bill_details(bill_id, pay_id)
print(details)
# خروجی: {'is_valid': True, 'amount_rial': 17701000, 'amount_toman': 1770100, 'type': 'تلفن ثابت', 'type_code': '4'}
```

### ۶. زمان نسبی و تقویم جلالی
```python
import parsikit
import datetime

# تبدیل تاریخ میلادی به جلالی با کش محاسباتی بسیار سریع
jy, jm, jd = parsikit.gregorian_to_jalali(2026, 7, 5)
print(parsikit.format_jalali(jy, jm, jd, "YYYY-MM-DD"))
# خروجی: "1405-04-14"

# بررسی سال‌های کبیسه جلالی (فرمول دقیق ۲۸۲۰ ساله نجومی)
print(parsikit.is_jalali_leap(1403)) # True

# تبدیل زمان به عبارت‌های توصیفی فارسی
posted_at = datetime.datetime.now() - datetime.timedelta(hours=3)
print(parsikit.humanize_relative_time(posted_at))
# خروجی: "۳ ساعت پیش"
```

### ۷. بهبود نمایش متون فارسی در سیستم‌های گرافیکی
```python
import parsikit

# چسباندن و پیوند حروف متناسب با اعراب بدون قطع اتصال حروف فارسی (Pillow, Pygame, OpenCV)
shaped = parsikit.reshape_for_graphics("عَلِیّ", reverse=False)
print(shaped) # "ﻋَﻠِﻲّ"

# شکستن پاراگراف‌های طولانی فارسی به خطوط منظم با تراز راست‌به‌چپ (RTL)
paragraph = "سلام جهان این یک متن بسیار طولانی برای تست بسته بندی خودکار خطوط فارسی است"
wrapped_lines = parsikit.reshape_paragraph_for_graphics(paragraph, max_chars_per_line=20)
for line in wrapped_lines:
    print(line)
```

### ۸. اتصال خودکار به فرم‌های کاربری (GUI Binding)
```python
# قالب‌بندی درجا و خودکار حین تایپ کاربر بدون خراب شدن موقعیت نشانگر موس
import parsikit
from PySide6.QtWidgets import QLineEdit, QApplication

app = QApplication([])
card_input = QLineEdit()

# کارت وارد شده حین تایپ به صورت خودکار به شکل "XXXX-XXXX-XXXX-XXXX" مرتب می‌شود
parsikit.bind_persian_input(card_input, "card_number")

card_input.show()
app.exec()
```

---

## 🧪 اجرای آزمون‌ها (Unit Tests)

برای بررسی و صحت عملکرد تمامی بخش‌ها به صورت محلی و خودکار، آزمون‌های یکپارچه پروژه را اجرا کنید:

```bash
python -m unittest test.py
# یا
python test.py
```

---

## 👨‍💻 نویسنده

**علی کامرانی**

* گیت‌هاب: [@MRThugh](https://github.com/MRThugh)
* ایمیل: [kamrani.exe@gmail.com](mailto:kamrani.exe@gmail.com)

---

## 📄 مجوز (License)

این پروژه تحت مجوز **MIT** منتشر شده است. استفاده، ویرایش و توسعه مجدد آن در پروژه‌های شخصی، تجاری و متن‌باز کاملاً آزاد و رایگان است.

---

**ParsiKit** — مسیر برنامه‌نویسی فارسی تمیزتر، حرفه‌ای‌تر و لذت‌بخش‌تر. 🚀
