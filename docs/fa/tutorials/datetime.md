# آموزش تقویم شمسی (جلالی) و زمان نسبی در پارسی‌کیت

ماژول `parsikit.datetime` تبدیل تاریخ میلادی و شمسی را بدون نیاز به هیچ پکیج سنگینی به صورت صفر-وابستگی (Zero-Dependency) با الگوریتم دقیق ۳۳ ساله جلالی در اختیارت قرار می‌ده.

---

## ۱. تبدیل میلادی به شمسی (`gregorian_to_jalali`)

ورودی: سال، ماه، روز میلادی.  
خروجی: تاپل سه‌تایی `(jy, jm, jd)` سال، ماه و روز شمسی.

```python
import parsikit

jy, jm, jd = parsikit.gregorian_to_jalali(2026, 7, 6)
print(f"تاریخ شمسی: {jy}/{jm}/{jd}")
# خروجی: 1405/4/15
```

---

## ۲. تبدیل شمسی به میلادی (`jalali_to_gregorian`)

```python
gy, gm, gd = parsikit.jalali_to_gregorian(1405, 4, 15)
print(f"تاریخ میلادی: {gy}-{gm:02d}-{gd:02d}")
# خروجی: 2026-07-06
```

تمام تبدیلات در بازه بیش از ۱۰۰ سال تست شده و کاملاً با تقویم رسمی مطابقت دارد.

---

## ۳. فرمت‌بندی تاریخ شمسی (`format_jalali`)

می‌تونی الگوهای مختلفی مثل `YYYY/MM/DD` یا `YYYY-MM-DD` بسازی:

```python
# الگوهای مختلف
print(parsikit.format_jalali(1403, 1, 5, pattern="YYYY/MM/DD"))  # '1403/01/05'
print(parsikit.format_jalali(1403, 1, 5, pattern="YYYY-MM-DD"))  # '1403-01-05'
print(parsikit.format_jalali(1403, 12, 29, pattern="DD/MM/YYYY")) # '29/12/1403'
```

---

## ۴. نام ماه‌های شمسی (`get_jalali_month_name`)

```python
print(parsikit.get_jalali_month_name(1))   # 'فروردین'
print(parsikit.get_jalali_month_name(7))   # 'مهر'
print(parsikit.get_jalali_month_name(12))  # 'اسفند'
```

---

## ۵. تشخیص سال کبیسه جلالی (`is_jalali_leap`)

سال کبیسه سالی است که اسفند ۳۰ روزه بوده و طول کل سال ۳۶۶ روز است:

```python
print(parsikit.is_jalali_leap(1399))  # True
print(parsikit.is_jalali_leap(1400))  # False
print(parsikit.is_jalali_leap(1403))  # True
print(parsikit.is_jalali_leap(1404))  # False
print(parsikit.is_jalali_leap(1408))  # True
```

---

## ۶. زمان نسبی به زبان فارسی (`humanize_relative_time`)

نمایش اختلاف زمان شبیه شبکه‌های اجتماعی («هم‌اکنون»، «۵ دقیقه پیش»، «دیروز»، «۱ سال قبل»):

```python
import datetime

now = datetime.datetime.now()

# ۵ ثانیه قبل
print(parsikit.humanize_relative_time(now - datetime.timedelta(seconds=5), reference=now))
# 'هم‌اکنون'

# ۵ دقیقه قبل (با ارقام فارسی)
print(parsikit.humanize_relative_time(now - datetime.timedelta(minutes=5), reference=now))
# '۵ دقیقه پیش'

# ۳ ساعت قبل
print(parsikit.humanize_relative_time(now - datetime.timedelta(hours=3), reference=now))
# '۳ ساعت پیش'

# دیروز
print(parsikit.humanize_relative_time(now - datetime.timedelta(days=1), reference=now))
# 'دیروز'

# ۵ روز قبل
print(parsikit.humanize_relative_time(now - datetime.timedelta(days=5), reference=now))
# '۵ روز پیش'
```
اگر پارامتر `reference` را پاس ندهی، به صورت پیش‌فرض از `datetime.datetime.now()` استفاده می‌شود.
