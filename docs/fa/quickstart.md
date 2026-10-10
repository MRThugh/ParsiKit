# شروع سریع با پارسی‌کیت (Quickstart)

بیا با چند مثال ساده و پرکاربرد شروع کنیم تا ببینی پارسی‌کیت چقدر کارهای روزمره پایتون رو راحت‌تر می‌کنه!

---

## ۱. تمیزکاری و استانداردسازی متن فارسی

یکی از رایج‌ترین مشکلات، کاراکترهای عربی («ي» و «ك») و نبود نیم‌فاصله است:

```python
import parsikit

dirty_text = "ي كافيه كتاب ها رو برداري و بيايي"
clean_text = parsikit.standardize_persian(dirty_text)

print(clean_text)
# خروجی: ی کافیه کتاب‌ها رو برداری و بیایی
```

دیدید؟ هم حروف «ی» و «ک» استاندارد فارسی شدند و هم نیم‌فاصله‌های «کتاب‌ها» و «بیایی» به درستی اصلاح شدند!

---

## ۲. اعتبارسنجی و فرمت‌بندی کد ملی

می‌تونی از تابع سریع یا از کلاس شیءگرای `NationalCode` استفاده کنی:

```python
import parsikit

# روش تابعی:
is_ok = parsikit.is_valid_national_code("7730123452")
print(is_ok)  # True

# روش شیءگرا:
nc = parsikit.NationalCode("7730123452")
print(nc.formatted)  # '773-012345-2'
print(nc.masked)     # '773-****45-2'
print(nc.clean)      # '7730123452'
```

حواست باشه اگه کد ملی نامعتبر باشه (مثلاً رقم کنترلیش نخونه یا ارقام تکراری باشه)، خطای `InvalidNationalCodeError` پرتاب می‌کنه.

---

## ۳. تبدیل عدد به حروف و نمایش مبالغ

نمایش قیمت به تومان یا ریال با ارقام فارسی:

```python
import parsikit

amount = 1250000  # تومان

# تبدیل به حروف فارسی
words = parsikit.number_to_words(amount)
print(words)  # 'یک میلیون و دویست و پنجاه هزار'

# فرمت مالی با ارقام فارسی
formatted = parsikit.format_currency(amount, currency="toman", persian_digits=True)
print(formatted)  # '۱،۲۵۰،۰۰۰ تومان'
```

---

## ۴. تبدیل تاریخ میلادی به شمسی

```python
import parsikit

# تبدیل تاریخ ۶ ژوئیه ۲۰۲۶
jy, jm, jd = parsikit.gregorian_to_jalali(2026, 7, 6)
print(f"{jy}/{jm}/{jd}")  # 1405/4/15

# نام ماه و سال کبیسه
print(parsikit.get_jalali_month_name(jm))  # 'تیر'
print("کبیسه است؟", parsikit.is_jalali_leap(jy))  # False
```

---

## ۵. زمان نسبی به زبان فارسی (Humanize)

```python
import datetime
import parsikit

now = datetime.datetime.now()
past_time = now - datetime.timedelta(minutes=5)

print(parsikit.humanize_relative_time(past_time, reference=now))
# خروجی: '۵ دقیقه پیش'
```

---

## گام بعدی چیه؟

حالا که دست‌گرمی داشتی، می‌تونی آموزش‌های عمیق‌تر هر بخش رو بخونی:
- [آموزش پردازش پیشرفته متن](tutorials/text_processing.md)
- [آموزش کامل اعتبارسنجی‌ها (کارت بانکی، شبا، پلاک و...)](tutorials/validation.md)
