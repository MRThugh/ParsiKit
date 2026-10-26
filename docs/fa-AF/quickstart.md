# رهنمود شروع سریع ParsiKit

در کمتر از ۵ دقیقه با بخش‌های اصلی کتابخانه‌ی ParsiKit آشنا شوید و اولین نمونه‌ها را اجرا کنید.

---

## ۱. معیارسازی و اصلاح متن

```python
import parsikit

# تبدیل حروف عربی و تنظیم فاصله‌های ناهماهنگ
raw_text = "ي كافيه كتاب ها رو برداري و بري"
clean_text = parsikit.standardize_persian(raw_text)

print(clean_text)
# خروجی: ی کافیه کتاب‌ها رو برداری و بری
```

---

## ۲. اعتبارسنجی کود ملی (کد ملی / شناسه)

```python
import parsikit

code = "0010123458"
nc = parsikit.NationalCode(code)

print(nc.is_valid)   # True (معتبر بودن بر اساس الگوریتم ریاضی)
print(nc.formatted)  # '001-012345-8'
print(nc.masked)     # '001-****45-8' (مناسب برای ثبت امن در لاگ‌ها)
print(nc.location)   # {'province': 'تهران', 'city': 'تهران مرکزی'}
```

---

## ۳. ارقام و محاسبات مالی

```python
import parsikit

amount = 1500000

# قالب‌بندی با ارقام فارسی و جداکننده‌ی هزارگان
formatted = parsikit.format_currency(amount, "toman", persian_digits=True)
print(formatted)
# خروجی: ۱،۵۰۰،۰۰۰ تومان

# تبدیل رقم به حروف نوشتاری
words = parsikit.number_to_words(amount)
print(f"{words} تومان")
# خروجی: یک میلیون و پانصد هزار تومان
```

---

## ۴. گاهشماری هجری شمسی و زمان نسبی

```python
import parsikit

# تبدیل تاریخ میلادی به هجری شمسی
jy, jm, jd = parsikit.gregorian_to_jalali(2026, 7, 6)
month_name = parsikit.get_jalali_month_name(jm)
print(f"{jd} {month_name} {jy}")
# خروجی: 15 تیر 1405

# بیان زمان نسبی به زبان طبیعی
print(parsikit.humanize_relative_time(-300))
# خروجی: ۵ دقیقه پیش
```

---

## ۵. شماره‌های مبایل و کارت‌های بانکی

```python
import parsikit

# شماره تلفون مبایل
mobile = parsikit.MobileNumber("09123456789")
print(mobile.international)  # '+989123456789'
print(mobile.operator)       # 'MCI'
print(mobile.masked)         # '0912***6789'

# کارت بانکی
card = parsikit.BankCard("6037991122334455")
print(card.bank_name)        # 'بانک ملی ایران'
print(card.formatted)        # '6037-9911-2233-4455'
print(card.masked)           # '6037-99**-****-4455'
```
