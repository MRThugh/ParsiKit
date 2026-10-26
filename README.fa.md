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
[![Official Website](https://img.shields.io/badge/وبسایت-parsikit-teal.svg)](https://mrthugh.github.io/parsikit-website/)

---

### 🌐 نسخه‌های زبان / Language Editions / Интихоби забон

| زبان | کد زبان | فایل README | هاب مستندات | جهت متن |
|---|---|---|---|---|
| **فارسی (ایران)** | `fa` | **[راهنمای فارسی](README.fa.md)** | [مستندات فارسی](docs/fa/index.md) | راست‌به‌چپ (RTL) |
| **دری (افغانستان)** | `fa-AF` | **[رهنمود دری](README.fa-AF.md)** | [مستندات دری](docs/fa-AF/index.md) | راست‌به‌چپ (RTL) |
| **Тоҷикӣ (Тоҷикистон)** | `tg` | **[Дастури тоҷикӣ](README.tg.md)** | [Ҳуҷҷатгузории тоҷикӣ](docs/tg/index.md) | چپ‌به‌راست (LTR) |
| **English** | `en` | **[English README](README.md)** | [English Docs](docs/en/index.md) | چپ‌به‌راست (LTR) |

---

**یک زیرساخت کدنویسی کامل، سریع و کاملاً پایتونی برای پردازش متن فارسی، اعتبارسنجی داده‌ها، محاسبات مالی، تقویم جلالی، عیب‌یابی متون فارسی و حفظ امنیت داده‌های حساس.**

</div>

---

## 🔗 پیوندهای رسمی پروژه

- **وب‌سایت رسمی مستندات**: [https://mrthugh.github.io/parsikit-website/](https://mrthugh.github.io/parsikit-website/)
- **مخزن سورس کتابخانه**: [https://github.com/MRThugh/ParsiKit](https://github.com/MRThugh/ParsiKit)
- **مخزن سورس وب‌سایت**: [https://github.com/MRThugh/parsikit-website](https://github.com/MRThugh/parsikit-website)
- **ثبت اشکال و پیشنهادات**: [https://github.com/MRThugh/ParsiKit/issues](https://github.com/MRThugh/ParsiKit/issues)
- **تاریخچه تغییرات نسخه‌ها**: [CHANGELOG.md](CHANGELOG.md)
- **راهنمای معماری سامانه**: [docs/development/architecture.md](docs/development/architecture.md)
- **راهنمای مشارکت در توسعه**: [docs/development/contributing.md](docs/development/contributing.md)

---

## 📖 معرفی پارسی‌کیت

کتابخانه‌ی **ParsiKit** (که در کدهایتان به صورت `parsikit` ایمپورت می‌کنید) یک ابزار همه‌فن‌حریف و بدون هیچ وابستگی خارجی (Zero-Dependency) است که طراحی شده تا تمام چالش‌های کار با داده‌های فارسی در برنامه‌نویسی پایتون را حل کند.

در نسخه **v3.3.1**، پارسی‌کیت از یک ابزار ساده فراتر رفته و به یک **زیرساخت برنامه‌نویسی همه‌جانبه** تبدیل شده است. اکنون علاوه بر معماری شیءگرا و یکپارچه، ابزارهای پیشرفته عیب‌یابی متن، فرمت‌دهی هوشمند و سازگار با تراز بصری فارسی، ابزارهای امنیتی (ماسک کردن اطلاعات) و تشخیص خودکار نوع داده‌ها در دسترس است تا بتوانید کدهای تمیزتر، امن‌تر و حرفه‌ای‌تری بنویسید.

---

## 🚀 ستون‌های اصلی پارسی‌کیت در نسخه v3.3.1

### ۱. تنظیمات سراسری و کش سریع (`parsikit.config` و `parsikit.cache`)
* **کش سریع و امن**: کارهای سنگین پردازشی (مثل تبدیل رقم‌های خیلی بزرگ به حروف فارسی یا محاسبات تاریخی) به صورت خودکار با یک سیستم کش روان و امن (Thread-safe) بهینه‌سازی می‌شوند تا سرعت برنامه‌تان به حداکثر برسد.
* **تنظیمات سراسری ساده**: نرخ مالیات، واحد پولی پیش‌فرض سیستم یا روشن/خاموش بودن کش را به راحتی در کل پروژه مدیریت کنید.

### ۲. ارورهای ساختاریافته ایرانی (`parsikit.exceptions`)
دیگر نیازی نیست نگران مدیریت ارورهای کلی پایتون مثل `ValueError` یا `TypeError` باشید. پارسی‌کیت ارورهای اختصاصی و منطبق با استانداردهای ایرانی (مثل کد ملی نامعتبر، کارت بانکی اشتباه و...) را در اختیارتان می‌گذارد که برای معماری‌های تمیز (Clean Architecture) فوق‌العاده است.

### ۳. مدل‌های دامنه شیءگرا (`parsikit.models`)
رشته‌های خام ورودی را داخل مدل‌های شیک و شیءگرا مثل `NationalCode` ،`MobileNumber` ،`BankCard` یا `VehiclePlate` قرار دهید. این مدل‌ها به محض ساخته شدن ورودی را اعتبارسنجی می‌کنند و متدهای جذابی مثل تشخیص اپراتور سیم‌کارت، استان صدور کد ملی یا جزئیات بانک صادرکننده‌ی کارت را به شما تحویل می‌دهند.

### ۴. ابزارهای عیب‌یابی و تراز بصری فارسی (`parsikit.dev`)
* **تراز بصری متن‌ها (`pformat` و `persian_fstring`)**: در حالت عادی، پایتون پهنای متون حاوی نیم‌فاصله یا اعراب را اشتباه حساب می‌کند و تراز خروجی‌ها یا جدول‌های ترمینال به هم می‌ریزد. پارسی‌کیت با حساب کردن پهنای واقعی کاراکترها روی مانیتور، خروجی‌های کاملاً تراز شده تحویلتان می‌دهد.
* **عیب‌یابی هوشمند متن**: متون ورودی را پایش کنید تا اگر کاراکترهای عربی مزاحم، نیم‌فاصله‌های فراموش‌شده یا فاصله‌های اضافی دارند، فوراً متوجه شوید و اصلاحشان کنید.

### ۵. پکیج امنیتی و پاکسازی پیشرفته (`parsikit.text` و `parsikit.validators`)
* **اسلاگ‌ساز سئو (`slugify`)**: متون فارسی یا ترکیبی را به اسلاگ‌های انگلیسی (Finglish) تمیز برای آدرس صفحات وب یا نام فایل‌ها تبدیل کنید (با ترجمه خودکار کلمات پرکاربرد مثل "سلام دنیا" به "salam-donya").
* **پاکسازی همه‌جانبه (`clean_text` و `normalize_whitespace`)**: فاصله‌های اضافی را حذف کنید، خطوط خالی را مرتب کنید، حروف عربی را به فارسی برگردانید و کدهای نامرئی یونیکد را از متن‌ها جارو کنید.
* **تشخیص‌دهنده هوشمند ورودی (`detect`)**: ورودی کاربر را پایش کنید تا سیستم خودش بفهمد دیتای ورودی ایمیل است، آی‌پی است، آدرس وب‌سایت، شماره موبایل، شبا یا کارت بانکی است.
* **مخفی‌سازی اطلاعات حساس (`mask_*`)**: شماره موبایل، کد ملی، ایمیل یا کارت بانکی کاربرها را قبل از نوشتن در لاگ‌ها یا نمایش در پنل کاربری، به راحتی ماسک و ایمن کنید (مثل `0912***6789`).

---

## ⚙️ نصب پارسی‌کیت

```bash
pip install parsikit
```

برای ارتقا به آخرین نسخه:
```bash
pip install --upgrade parsikit
```

**نیازمند پایتون نسخه 3.10 به بالا** (آزمایش‌شده روی پایتون 3.10، 3.11، 3.12 و 3.13)

برای مشاهده روش‌های دیگر نصب (Poetry, uv, venv یا سورس گیت‌هاب)، به [راهنمای نصب](docs/fa/installation.md) مراجعه فرمایید.

---

## 🛠️ مدیریت تنظیمات سراسری و ارورها

### ۱. تنظیم سراسری رفتار کتابخانه
```python
import parsikit

# تنظیم سراسری نرخ مالیات بر ارزش افزوده (پیش‌فرض: 0.10)
parsikit.config.default_tax_rate = 0.09

# تنظیم واحد پولی پیش‌فرض در سراسر برنامه (پیش‌فرض: toman)
parsikit.config.default_currency = "rial"

# فعال‌سازی کش پردازشی برای سرعت بیشتر
parsikit.config.enable_cache = True
```

### ۲. ساختار ارورهای اختصاصی
همه ارورهای پارسی‌کیت از `ValidationError` ارث‌بری می‌کنند تا به راحتی بتوانید خطاهای دیتای ورودی را مدیریت کنید:
```python
import parsikit

try:
    card = parsikit.BankCard("invalid-card-number")
except parsikit.InvalidCardNumberError as e:
    print(f"شماره کارت اشتباه است: {e}")
except parsikit.ValidationError as e:
    print(f"یک خطای اعتبارسنجی رخ داد: {e}")
```

---

## 🦄 هماهنگی بومی با Pydantic v2 و FastAPI

شما می‌توانید کلاس‌های پارسی‌کیت را مستقیماً به عنوان نوع فیلدها در اسکیماهای Pydantic یا ورودی متدهای FastAPI قرار دهید. کتابخانه خودش کار ولیدیشن، تبدیل فرمت و ارسال خطاهای تمیز به کاربر را انجام می‌دهد:

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
    # تمام داده‌ها از قبل ولیدیت، تمیز و استاندارد شده‌اند!
    print(user.fullname.standardize()) # تصحیح ی/ک و نیم‌فاصله‌ها
    print(user.national_id.location)   # خروجی: {"province": "تهران", "city": "تهران مرکزی"}
    print(user.phone.to_international()) # خروجی: "+989123456789"
    
    # خروجی گرفتن به صورت دیکشنری پایتون
    return {
        "status": "success",
        "data": {
            "national_id": user.national_id.to_dict(),
            "card_bank": user.card.bank
        }
    }
```

---

## 🚀 راهنمای ویژگی‌ها و نمونه کدها

### ۱. دستیار توسعه‌دهنده و خطایاب متون (`parsikit.dev`)
پارسی‌کیت ابزارهای کارآمدی را برای تست، خطایابی و نمایش متون فارسی در ترمینال فراهم کرده است.

#### عیب‌یابی گام‌به‌گام متن
تک‌تک باگ‌های ساختاری متن را پیدا کنید و راهکار اصلاحش را تحویل بگیرید:
```python
import parsikit

# بررسی خطاهای یونیکد و نیم‌فاصله
analysis = parsikit.inspect_text("ي كافيه ك کتاب ها ميباشد ۱۲۳")
print(analysis["has_arabic_chars"]) # خروجی: True (به خاطر ي و ك عربی)
print(analysis["has_zwnj_issues"])  # خروجی: True (به خاطر "کتاب ها" و "ميباشد")
print(analysis["suggestions"])
# خروجی: لیستی از راهکارهای پیشنهادی برای تصحیح حروف عربی، نیم‌فاصله‌ها و تبدیل اعداد

# چاپ گزارش رنگی و شکیل در ترمینال
parsikit.debug_text("ي كافيه ك کتاب ها ميباشد")
```

#### نمایش خوانای فارسی در لاگ‌ها و ترمینال
در حالت عادی، پایتون متون فارسی داخل لیست یا دیکشنری را به صورت کدهای ناخوانای یونیکد (مثل `\u0627`) نشان می‌دهد. پارسی‌کیت این مشکل را حل کرده است:
```python
import parsikit

data = {"کاربر": ["امیر", "رضا"], "وضعیت": True}

# خروجی پایتون در حالت عادی ناخواناست، اما با ابزار ما:
print(parsikit.persian_repr(data))
# خروجی: {'کاربر': ['امیر', 'رضا'], 'وضعیت': True}

# چاپ ساختاریافته، منظم و رنگی داده‌ها در خروجی
parsikit.pretty_print(data, title="اطلاعات کاربران")
```

#### اعتبارسنجی دسته‌ای داده‌ها (Batch)
یک لیست بزرگ از دیتای خام را همزمان ولیدیت کنید و گزارش تمیزی از موارد موفق و خطاها بگیرید:
```python
import parsikit

items = ["7730123452", "1111111111", "0010123451", "bad-code"]
report = parsikit.validate_batch(items, parsikit.NationalCode, silent=False)
# یک جدول و گزارش منظم از موارد معتبر و نامعتبر در ترمینال چاپ می‌کند
```

#### لاگ‌های فارسی شیک و تمیز
لاگر پیش‌فرض سیستم را طوری تنظیم کنید که کدهای ناخوانا تولید نکند و فارسی را تمیز نمایش دهد:
```python
import parsikit

logger = parsikit.setup_logging("DEBUG")
logger.info("ثبت نام کاربر با موفقیت انجام شد.")
```

---

### ۲. فرمت‌دهی و تراز بصری فارسی (`pformat` و `persian_fstring`)
کاراکترهایی مثل نیم‌فاصله یا اعراب، پهنای فیزیکی روی مانیتور ندارند اما ایندکس رشته را پر می‌کنند که باعث می‌شود تراز ستون‌ها به هم بریزد. پارسی‌کیت این محاسبات را اصلاح می‌کند.

#### تراز بی‌نقص متون حاوی نیم‌فاصله و اعراب
```python
import parsikit

# کلمه "کتاب‌‌ها" دارای نیم‌فاصله است (طول واقعی رشته 8 کاراکتر، اما پهنای دیداری آن 7 کاراکتر است)
# متد pformat پهنای دیداری را ملاک قرار می‌دهد و ستون‌ها را دقیقاً تراز می‌کند:
aligned = parsikit.pformat("{:<10} | تراز شد", "کتاب‌‌ها")
print(aligned) # خروجی: "کتاب‌‌ها   | تراز شد"
```

#### تبدیل سریع اعداد به فارسی با پسوند قالب‌بندی
کافی است پسوند `fa` یا `p` را به قالب‌هایتان اضافه کنید تا ارقام به صورت خودکار فارسی‌سازی شوند:
```python
import parsikit

# فرمت سه رقم سه رقم عدد و تبدیل همزمان به ارقام فارسی
print(parsikit.pformat("هزینه: {:>10,fa} ریال", 1500000))
# خروجی: "هزینه:  ۱،۵۰۰،۰۰۰ ریال"
```

#### فرمت‌دهی هوشمند شبیه به f-string پایتون
بدون نیاز به پاس دادن تک‌تک متغیرها، متغیرهای محلی و محیطی شما را خودش تشخیص می‌دهد:
```python
import parsikit

name = "علی"
price = 12500

# به طور خودکار مقادیر name و price را از اسکوپ برنامه می‌خواند و تراز می‌کند:
formatted = parsikit.persian_fstring("کاربر: {name:<5} | قیمت: {price:fa} تومان")
print(formatted)
# خروجی: "کاربر: علی   | قیمت: ۱۲۵۰۰ تومان"
```

---

### ۳. اسلاگ‌ساز، فضاها و پاکسازی همه‌جانبه متن
پاکسازی کامل متن‌ها، تولید لینک‌های سئو و ذخیره دیتای استاندارد در دیتابیس.

#### ساخت اسلاگ‌های فینگلیش برای آدرس صفحات (SEO)
متون فارسی را به بهترین معادل پینگلیش برای آدرس صفحات وب یا آدرس تصاویر تبدیل می‌کند:
```python
import parsikit

# کلمات پرکاربرد را خودش ترجمه می‌کند و بقیه کاراکترها را به فینگلیش شیک تبدیل می‌کند
print(parsikit.slugify("آموزش وردپرس به زبان ساده"))
# خروجی: "amoozesh-wordpress-beh-zaban-sadeh"

print(parsikit.slugify("سلام دنیا 💕"))
# خروجی: "salam-donya"
```

#### پاکسازی و نویزگیری کامل متن (`clean_text`)
یک ابزار کامل برای دیتابیس! کاراکترهای عربی را فارسی می‌کند، نیم‌فاصله‌ها را اصلاح می‌کند، ارقام را فارسی می‌کند و کدهای مزاحم یونیکد را دور می‌ریزد:
```python
import parsikit

dirty_text = "ي كافيه ك   کتاب  ها  ميباشد  ۱۱۲۳\n\n\n\nجدید  "
print(parsikit.clean_text(dirty_text))
# خروجی:
# "ی کافیه ک کتاب‌ها میباشد ۱۱۲۳
# 
# جدید"
```

#### نرمال‌سازی فضاهای خالی و پاراگراف‌ها
فاصله‌ها و خطوط خالی اضافی را مدیریت کنید، با قابلیت حفظ ساختار پاراگراف‌ها یا مسطح‌سازی کل متن:
```python
import parsikit

raw_paragraphs = "خط اول\n\n\n\nخط دوم   با   فاصله\n\nخط سوم"

# حفظ فاصله‌ی بین پاراگراف‌ها (تبدیل خطوط خالی زیاد به تک خط خالی)
print(parsikit.normalize_whitespace(raw_paragraphs, keep_paragraphs=True))
# خروجی:
# "خط اول
# 
# خط دوم با فاصله
# 
# خط سوم"

# تبدیل کل متن به یک خط صاف بدون لاین بریک
print(parsikit.normalize_whitespace(raw_paragraphs, keep_paragraphs=False))
# خروجی: "خط اول خط دوم با فاصله خط سوم"
```

#### مبدل سراسری اعداد متن به فارسی یا انگلیسی
```python
import parsikit

text = "شماره تماس ما: 09123456789"
print(parsikit.convert_numbers(text, to="persian"))
# خروجی: "شماره تماس ما: ۰۹۱۲۳۴۵۶۷۸۹"

print(parsikit.convert_numbers("کد امنیتی: ۱۲۵۰۰", to="english"))
# خروجی: "کد امنیتی: 12500"
```

---

### ۴. اعتبارسنجی هوشمند و مخفی‌سازی اطلاعات حساس
ورودی‌ها را اتوماتیک تشخیص دهید و دیتای حساس کاربران را در کمال امنیت لاگ یا ذخیره کنید.

#### تشخیص‌دهنده‌ی هوشمند نوع داده ورودی (`detect`)
تک فرم‌های ورودی را به صورت پویا کلاس‌بندی و شناسایی کنید:
```python
import parsikit

print(parsikit.detect("09123456789")) # خروجی: "mobile_number"
print(parsikit.detect("7730123452"))  # خروجی: "national_code"
print(parsikit.detect("ali@example.com")) # خروجی: "email"
print(parsikit.detect("192.168.1.1")) # خروجی: "ip" (پشتیبانی کامل از IPv4 و IPv6)
print(parsikit.detect("https://google.com")) # خروجی: "url"
print(parsikit.detect("یک جمله ساده")) # خروجی: None
```

#### ابزارهای مخفی‌سازی و ماسک کردن داده‌ها (Security)
بخش‌های حساس دیتای کاربرها را قبل از نمایش عمومی یا ذخیره در فایل‌های لاگ ماسک کنید:
```python
import parsikit

# ماسک کردن شماره موبایل
print(parsikit.mask_mobile("09123456789"))
# خروجی: "0912***6789"

# ماسک کردن کارت بانکی (با حفظ قالب‌بندی استاندارد چانک‌ها)
print(parsikit.mask_card("6037991122334455", mask_char="X"))
# خروجی: "6037-99XX-XXXX-4455"

# ماسک کردن کد ملی (با حفظ قالب تراز شده)
print(parsikit.mask_national_code("7730123452"))
# خروجی: "773-****45-2"

# ماسک کردن آدرس ایمیل به صورت متناسب
print(parsikit.mask_email("kamrani.exe@gmail.com"))
# خروجی: "ka******e@gmail.com"
```

---

### ۵. مبدل تقویم، ابزارهای مالی، مرتب‌سازی و ری‌شیپر (قابلیت‌های پایدار)
تمام قابلیت‌های قدرتمند نسخه‌های قبلی همچنان با همان ثبات و بدون هیچ تغییری پشتیبانی می‌شوند.

#### مبدل تقویم جلالی و زمان انسان‌پسند
```python
import parsikit
import datetime

# تبدیل میلادی به جلالی با سرعت بسیار بالا به دلیل استفاده از کش سیستم
jy, jm, jd = parsikit.gregorian_to_jalali(2026, 7, 5)
print(parsikit.format_jalali(jy, jm, jd, "YYYY-MM-DD"))
# خروجی: "1405-04-14"

# بررسی سال کبیسه جلالی
print(parsikit.is_jalali_leap(1403)) # خروجی: True

# نمایش زمان نسبی به زبان فارسی
posted_at = datetime.datetime.now() - datetime.timedelta(hours=3)
print(parsikit.humanize_relative_time(posted_at))
# خروجی: "۳ ساعت پیش"
```

#### بازآرایی متون برای موتورهای گرافیکی (Reshaper)
متون فارسی را برای رندر کردن صحیح در موتورهایی که راست‌چین یا اتصال حروف را پشتیبانی نمی‌کنند (مثل Pillow ،Pygame یا OpenCV) آماده کنید:
```python
import parsikit

shaped = parsikit.reshape_for_graphics("عَلِیّ", reverse=False)
print(shaped) # خروجی: "ﻋَﻠِﻲّ"
```

#### تراز بومی فیلدهای ورودی در GUI (Tkinter / PyQt / PySide)
تصحیح فرمت فیلدها و فاصله‌گذاری‌ها دقیقاً در همان لحظه‌ای که کاربر تایپ می‌کند، با حفظ موقعیت مکان‌نما (Cursor):
```python
import parsikit
from PySide6.QtWidgets import QLineEdit, QApplication

app = QApplication([])
card_input = QLineEdit()

# اصلاح خودکار ورودی کارت بانکی به محض تایپ کاربر به صورت "XXXX-XXXX-XXXX-XXXX"
parsikit.bind_persian_input(card_input, "card_number")

card_input.show()
app.exec()
```

---

## 🧪 اجرای تست‌ها

یک مجموعه‌ی کامل و بدون خطای تست (Unit Test) در روت پروژه قرار دارد تا سلامت ساختاری کتابخانه را در محیط شما تایید کند:

```bash
python -m unittest test.py
# یا
pytest -v tests
```

---

## 👨‍💻 توسعه‌دهنده

**علی کامرانی**

- گیت‌هاب: [@MRThugh](https://github.com/MRThugh)
- ایمیل: kamrani.exe@gmail.com
- وب‌سایت مستندات: [https://mrthugh.github.io/parsikit-website/](https://mrthugh.github.io/parsikit-website/)

---

## 📄 لایسنس

این پروژه تحت لایسنس معتبر **MIT** منتشر شده است. استفاده، تغییر و انتشار این کتابخانه در تمامی پروژه‌های شخصی، تجاری و متن‌باز شما کاملاً آزاد و رایگان است.

---

**پارسی‌کیت** — توسعه نرم‌افزارهای فارسی را برای شما ساده‌تر، تمیزتر و لذت‌بخش‌تر می‌کند. 🚀