<div align="center">

# 🌟 کتابخانه‌ی ParsiKit 🌟
<p align="center">
  <img 
    src="https://raw.githubusercontent.com/MRThugh/MRThugh/main/badge.svg"
    width="50%" 
    alt="نشان پارسی‌کیت"
  />
</p>

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Author](https://img.shields.io/badge/author-Ali%20Kamrani-purple.svg)](https://github.com/MRThugh)
[![Version](https://img.shields.io/badge/version-3.3.1-blue.svg)](https://github.com/MRThugh/ParsiKit)
[![Official Website](https://img.shields.io/badge/ویبسایت-parsikit-teal.svg)](https://mrthugh.github.io/parsikit-website/)

---

### 🌐 نسخه‌های زبان / Language Editions / Интихоби забон

| زبان | کود زبان | فایل README | هاب مستندات | جهت متن |
|---|---|---|---|---|
| **دری (افغانستان)** | `fa-AF` | **[رهنمود دری](README.fa-AF.md)** | [مستندات دری](docs/fa-AF/index.md) | راست‌به‌چپ (RTL) |
| **فارسی (ایران)** | `fa` | **[راهنمای فارسی](README.fa.md)** | [مستندات فارسی](docs/fa/index.md) | راست‌به‌چپ (RTL) |
| **Тоҷикӣ (Тоҷикистон)** | `tg` | **[Дастури тоҷикӣ](README.tg.md)** | [Ҳуҷҷатгузории тоҷикӣ](docs/tg/index.md) | چپ‌به‌راست (LTR) |
| **English** | `en` | **[English README](README.md)** | [English Docs](docs/en/index.md) | چپ‌به‌راست (LTR) |

---

**یک زیرساخت برنامه‌نویسی معیاری، پُرشتاب و کاملاً مبتنی بر پایتون برای پروسس متن، اعتبارسنجی داده‌ها، محاسبات مالی، تقویم هجری شمسی، بازآرایی دیداری متن‌های گرافیکی، عیب‌یابی و حفظ مصئونیت داده‌های حساس.**

</div>

---

## 🔗 پیوندهای رسمی پروژه

- **ویبسایت رسمی مستندات**: [https://mrthugh.github.io/parsikit-website/](https://mrthugh.github.io/parsikit-website/)
- **مخزن سورس کتابخانه در گیت‌هاب**: [https://github.com/MRThugh/ParsiKit](https://github.com/MRThugh/ParsiKit)
- **مخزن سورس ویبسایت**: [https://github.com/MRThugh/parsikit-website](https://github.com/MRThugh/parsikit-website)
- **بخش ثبت مشکلات و پیشنهادات**: [https://github.com/MRThugh/ParsiKit/issues](https://github.com/MRThugh/ParsiKit/issues)
- **تاریخچه‌ی تغییرات نسخه‌ها**: [CHANGELOG.md](CHANGELOG.md)
- **معماری سیستم و ساختار داخلی**: [docs/development/architecture.md](docs/development/architecture.md)
- **رهنمود سهم‌گیری و مشارکت**: [docs/development/contributing.md](docs/development/contributing.md)

---

## 📖 معرفی پارسی‌کیت (ParsiKit)

کتابخانه‌ی **ParsiKit** (که در برنامه‌های پایتون به نام `parsikit` فراخوانی می‌شود)، یک ابزار کاری همه‌جانبه، مستقل و بدون نیاز به بسته‌های خارجی (Zero-Dependency) می‌باشد که برای حل چالش‌های روزمره‌ی پروسس داده‌های فارسی و دری در محیط پایتون طرح‌ریزی شده است.

در نگارش **v3.3.1**، پارسی‌کیت به یک **زیرساخت برنامه‌سازی کامل و مسلکی** مبدل گردیده است. علاوه بر مودل‌های شی‌گرا و رابط کاربری یکپارچه، ابزارهای پیشرفته‌ی عیب‌یابی متن، قالب‌بندی هوشمند و سازگار با تراز دیداری حروف، ابزارهای مصئونیت (پوشاندن معلومات محرمانه) و تشخیص خودکار نوعیت داده‌ها فراهم شده تا برنامه‌نویسان بتوانند برنامه‌های باکیفیت‌تر، امن‌تر و منظم‌تر توسعه دهند.

---

## 🚀 ستون‌های اساسی معماری در نسخه v3.3.1

### ۱. تنظیمات عمومی و کش (Cache) مصئون چندریسمانی (`parsikit.config` و `parsikit.cache`)
* **حافظه موقت پرشتاب و مصئون**: محاسبات تکراری و سنگین (مانند تبدیل ارقام بسیار بزرگ به حروف یا سنجش تاریخ‌ها) با یک سیستم کش داخلی (Thread-safe LRU) سرعت داده می‌شوند.
* **تنظیمات عمومی آسان**: نرخ مالیات بر ارزش افزوده، واحد پولی پیش‌فرض یا فعال/غیرفعال بودن کش را در سراسر پروژه مدیریت نمایید.

### ۲. استثنائات و خطاهای ساختاریافته (`parsikit.exceptions`)
نیازی به مواجهه با خطاهای عمومی پایتون همچون `ValueError` نیست. پارسی‌کیت یک سلسله استثنائات اختصاصی و واضح (مانند نامعتبر بودن کارت بانکی یا کود ملی) را در اختیار شما می‌گذارد که برای معماری تمیز (Clean Architecture) بسیار مناسب است.

### ۳. مودل‌های دامنه شی‌گرا (`parsikit.models`)
رشته‌های ورودی خام را به مودل‌های ساختاریافته تبدیل نمایید، مانند `NationalCode` ،`MobileNumber` ،`BankCard` یا `VehiclePlate`. این مودل‌ها هنگام ایجاد شدن صحت داده را بررسی کرده و ویژگی‌هایی همچون نام بانک صادرکننده، نوعیت اپراتور یا ولایت صدور را استخراج می‌کنند.

### ۴. عیب‌یابی متن و تراز دیداری (`parsikit.dev`)
* **تراز دیداری متن‌ها (`pformat` و `persian_fstring`)**: در حالت عادی، پایتون به دلیل وجود کاراکترهای با پهنای صفر (نیم‌فاصله یا اعراب) پهنای فیزیکی حروف روی صفحه را درست محاسبه نکرده و ستون‌های جدول‌ها ناهمگون می‌شوند. پارسی‌کیت پهنای واقعی دیداری را محاسبه کرده و ستون‌ها را کاملاً تراز می‌سازد.
* **بررسی هوشمند کاستی‌های متن**: متن‌ها را جهت دریافت حروف عربی ناخواسته، فاصله‌های اضافی و نیم‌فاصله‌های فراموش‌شده بررسی نموده و راهکار اصلاحی دریافت دارید.

### ۵. پاک‌کاری پیشرفته، اسلاگ سئو و مصئونیت داده‌ها (`parsikit.text` و `parsikit.validators`)
* **تولید اسلاگ‌های سئو (`slugify`)**: تبدیل عنوان‌های متنی به اسلاگ‌های معیاری انگلیسی بر مبنای واژه‌نامه‌ی ترانسکریپشن واژه‌های پرکاربرد.
* **پاک‌کاری کلی متن (`clean_text` و `normalize_whitespace`)**: حذف کدهای نامرئی یونیکد، تنظیم نیم‌فاصله‌ها، اصلاح فاصله‌های اضافی میان پاراگراف‌ها و یکدست‌سازی حروف.
* **شناسایی خودکار نوع داده (`detect`)**: تحلیل خودکار ورودی برای تشخیص ایمیل، آدرس اینترنتی، شماره مبایل، کارت بانکی، شبا یا آی‌پی (IP).
* **پوشاندن معلومات حساس (`mask_*`)**: پنهان‌سازی بخش‌های میانی شماره‌های تلفون، کودهای شناسایی، کارت‌های بانکی و ایمیل‌ها جهت ثبت امن در لاگ‌ها (مانند `0912***6789`).

---

## ⚙️ رهنمود نصب

```bash
pip install parsikit
```

جهت ارتقا به تازه‌ترین نسخه:
```bash
pip install --upgrade parsikit
```

**نیازمند پایتون نگارش 3.10 و بالاتر** (آزمایش‌شده روی پایتون 3.10، 3.11، 3.12 و 3.13)

برای مطالعه‌ی دیگر روش‌های نصب (Poetry, uv, venv و سورس گیت‌هاب)، به [رهنمود نصب](docs/fa-AF/installation.md) مراجعه کنید.

---

## 🛠️ مدیریت تنظیمات عمومی و استثنائات

### ۱. عیارسازی تنظیمات عمومی
```python
import parsikit

# تنظیم عمومی نرخ مالیات (پیش‌فرض: 0.10)
parsikit.config.default_tax_rate = 0.09

# تعیین واحد پولی پیش‌فرض سیستم (پیش‌فرض: toman)
parsikit.config.default_currency = "rial"

# فعال‌سازی کش پرشتاب جهت بالا بردن بازدهی
parsikit.config.enable_cache = True
```

### ۲. ساختار استثنائات اختصاصی
تمامی خطاهای اختصاصی از صنف پایه‌ای `ValidationError` ارث‌بری می‌نمایند:
```python
import parsikit

try:
    card = parsikit.BankCard("invalid-card-number")
except parsikit.InvalidCardNumberError as e:
    print(f"شماره‌ی کارت نادرست است: {e}")
except parsikit.ValidationError as e:
    print(f"خطای عمومی اعتبارسنجی: {e}")
```

---

## 🦄 هماهنگی بومی با Pydantic v2 و FastAPI

شما می‌توانید مودل‌های پارسی‌کیت را مستقیماً منحیث نوعیت فیلدها در اسکیماهای Pydantic و اندپاینت‌های FastAPI به کار ببرید:

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
    # تمام داده‌ها قبلاً تصدیق، پاک‌کاری و معیارسازی شده‌اند!
    print(user.fullname.standardize()) # معیارسازی حروف و نیم‌فاصله‌ها
    print(user.national_id.location)   # موقعیت جغرافیایی
    print(user.phone.to_international()) # فرمت بین‌المللی: "+989123456789"
    
    # خروجی به صورت دیکشنری پایتون
    return {
        "status": "success",
        "data": {
            "national_id": user.national_id.to_dict(),
            "card_bank": user.card.bank
        }
    }
```

---

## 🚀 نمونه کودها و رهنمود قابلیت‌ها

### ۱. ابزارهای عیب‌یابی توسعه‌دهنده‌گان (`parsikit.dev`)
پارسی‌کیت مجموعه‌ای از امکانات کاربردی را برای آزمایش، خطایابی و نمایش درست متن‌ها در ترمینال فراهم آورده است.

#### عیب‌یابی تفصیلی متن
بررسی نقایص ساختاری متن و دریافت پیشنهادهای اصلاحی:
```python
import parsikit

analysis = parsikit.inspect_text("ي كافيه ك کتاب ها ميباشد ۱۲۳")
print(analysis["has_arabic_chars"]) # خروجی: True (به سبب حروف ي و ك)
print(analysis["has_zwnj_issues"])  # خروجی: True
print(analysis["suggestions"])
# رهنمودهای پیشنهادی جهت اصلاح حروف و نیم‌فاصله‌ها

# چاپ گزارش دیداری و رنگه در ترمینال
parsikit.debug_text("ي كافيه ك کتاب ها ميباشد")
```

#### نمایش خوانای فارسی در لاگ‌ها
در پایتون، متون داخل لست‌ها یا دیکشنری‌ها به شکل کدهای ناخوانا نمایش داده می‌شوند. پارسی‌کیت این مسأله را حل کرده است:
```python
import parsikit

data = {"کاربر": ["امیر", "احمد"], "وضعیت": True}

# نمایش تمیز و درست بدون کدهای اسکیپ
print(parsikit.persian_repr(data))
# خروجی: {'کاربر': ['امیر', 'احمد'], 'وضعیت': True}

# چاپ جدول‌بندی‌شده و رنگه
parsikit.pretty_print(data, title="معلومات کاربر")
```

#### اعتبارسنجی دسته‌ای داده‌ها (Batch Validation)
اعتبارسنجی یکجای مقادیر فراوان داده با ارائه‌ی گزارش خلاصه:
```python
import parsikit

items = ["7730123452", "1111111111", "0010123451", "bad-code"]
report = parsikit.validate_batch(items, parsikit.NationalCode, silent=False)
```

#### تنظیم لاگر معیاری برای نمایش متن‌ها
```python
import parsikit

logger = parsikit.setup_logging("DEBUG")
logger.info("ثبت‌نام با موفقیت انجام گردید.")
```

---

### ۲. تراز دیداری متن‌ها (`pformat` و `persian_fstring`)
کاراکترهایی چون نیم‌فاصله یا اعراب، جایگاه اندیکس را پر می‌سازند ولی در نمایش پهنایی ندارند که این امر چینش جدول‌ها را برهم می‌زند. پارسی‌کیت این نقص را رفع می‌نماید:

#### تنظیم دقیق پهنا با در نظر داشتن نیم‌فاصله
```python
import parsikit

# کلمه‌ی "کتاب‌‌ها" دارای نیم‌فاصله است
aligned = parsikit.pformat("{:<10} | تراز شد", "کتاب‌‌ها")
print(aligned) # "کتاب‌‌ها   | تراز شد"
```

#### تبدیل ارقام به فارسی از طریق پسوند
```python
import parsikit

# جداسازی سه رقمی و تبدیل به ارقام فارسی
print(parsikit.pformat("هزینه: {:>10,fa} ریال", 1500000))
# خروجی: "هزینه:  ۱،۵۰۰،۰۰۰ ریال"
```

#### قالب‌بندی خودکار با خوانش متغیرهای محیطی
```python
import parsikit

name = "احمد"
price = 12500

formatted = parsikit.persian_fstring("کاربر: {name:<5} | قیمت: {price:fa} افغانی/تومان")
print(formatted)
```

---

### ۳. اسلاگ‌ساز سئو و پاک‌کاری متن
تولید آدرس‌های صفحات اینترنتی و ذخیره‌سازی داده‌های تمیز در پایگاه داده.

#### اسلاگ‌های انگلیسی مناسب برای سئو (SEO)
```python
import parsikit

print(parsikit.slugify("آموزش پایتون به زبان ساده"))
# خروجی: "amoozesh-python-beh-zaban-sadeh"

print(parsikit.slugify("سلام دنیا 💕"))
# خروجی: "salam-donya"
```

#### پالایش و پاک‌کاری همه‌جانبه‌ی متن (`clean_text`)
```python
import parsikit

dirty_text = "ي كافيه ك   کتاب  ها  ميباشد  ۱۱۲۳\n\n\n\nجدید  "
print(parsikit.clean_text(dirty_text))
```

#### تنظیم فاصله‌ها و شکست خطوط
```python
import parsikit

raw_paragraphs = "خط اول\n\n\n\nخط دوم   با   فاصله\n\nخط سوم"
print(parsikit.normalize_whitespace(raw_paragraphs, keep_paragraphs=True))
```

#### تبدیل سراسری ارقام متن به فارسی یا انگلیسی
```python
import parsikit

text = "شماره‌ی تماس: 0791234567"
print(parsikit.convert_numbers(text, to="persian"))
print(parsikit.convert_numbers("کود امنیتی: ۱۲۵۰۰", to="english"))
```

---

### ۴. اعتبارسنجی هوشمند و پوشاندن معلومات محرمانه

#### تشخیص خودکار نوعیت داده (`detect`)
```python
import parsikit

print(parsikit.detect("09123456789")) # "mobile_number"
print(parsikit.detect("7730123452"))  # "national_code"
print(parsikit.detect("ali@example.com")) # "email"
print(parsikit.detect("192.168.1.1")) # "ip"
print(parsikit.detect("https://google.com")) # "url"
```

#### ابزارهای ماسک‌کردن معلومات حساس
```python
import parsikit

# پوشاندن شماره‌ی مبایل
print(parsikit.mask_mobile("09123456789"))
# خروجی: "0912***6789"

# پوشاندن کارت بانکی
print(parsikit.mask_card("6037991122334455", mask_char="X"))
# خروجی: "6037-99XX-XXXX-4455"

# پوشاندن کود شناسایی
print(parsikit.mask_national_code("7730123452"))
# خروجی: "773-****45-2"

# پوشاندن ایمیل
print(parsikit.mask_email("kamrani.exe@gmail.com"))
# خروجی: "ka******e@gmail.com"
```

---

### ۵. تقویم هجری شمسی، ابزارهای مالی و بازآرایی گرافیکی

#### تبدیل تقویم هجری شمسی و نمایش زمان نسبی
```python
import parsikit
import datetime

# تبدیل تاریخ میلادی به هجری شمسی با بهره‌گیری از کش
jy, jm, jd = parsikit.gregorian_to_jalali(2026, 7, 5)
print(parsikit.format_jalali(jy, jm, jd, "YYYY-MM-DD"))
# خروجی: "1405-04-14"

# بررسی سال کبیسه
print(parsikit.is_jalali_leap(1403)) # True

# بیان زمان نسبی به زبان طبیعی
posted_at = datetime.datetime.now() - datetime.timedelta(hours=3)
print(parsikit.humanize_relative_time(posted_at))
# خروجی: "۳ ساعت پیش"
```

#### بازآرایی متن برای موتورهای گرافیکی (Reshaper)
آماده‌سازی خط پیوسته برای محیط‌هایی که راست‌نویسی را پشتیبانی نمی‌کنند (همچون Pillow ،Pygame و OpenCV):
```python
import parsikit

shaped = parsikit.reshape_for_graphics("عَلِیّ", reverse=False)
print(shaped) # "ﻋَﻠِﻲّ"
```

#### ارتباط با واسط‌های گرافیکی (Tkinter / PyQt / PySide)
```python
import parsikit
from PySide6.QtWidgets import QLineEdit, QApplication

app = QApplication([])
card_input = QLineEdit()

# قالب‌بندی خودکار ارقام ورودی حین نوشتن
parsikit.bind_persian_input(card_input, "card_number")

card_input.show()
app.exec()
```

---

## 🧪 اجرای تست‌ها و آزمایش‌ها

مجموعه‌ای از تست‌های سنجش کیفیت (Unit Test) در روت پروژه موجود است:

```bash
python -m unittest test.py
# یا
pytest -v tests
```

---

## 👨‍💻 پدیدآورنده و طراح

**علی کامرانی (Ali Kamrani)**

- گیت‌هاب: [@MRThugh](https://github.com/MRThugh)
- ایمیل: kamrani.exe@gmail.com
- ویبسایت رسمی مستندات: [https://mrthugh.github.io/parsikit-website/](https://mrthugh.github.io/parsikit-website/)

---

## 📄 جوازنامه (License)

این پروژه بر بنیاد جوازنامه‌ی آزاد **MIT** نشر شده است. استفاده، تعدیل و توزیع این کتابخانه در برنامه‌های تجاری، شخصی و متن‌باز کاملاً رایگان و آزاد می‌باشد.

---

**پارسی‌کیت** — معیارسازی و ساده‌سازی پروسس داده‌های فارسی و دری در دنیای برنامه‌نویسی. 🚀
