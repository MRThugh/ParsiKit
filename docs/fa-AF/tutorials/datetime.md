# آموزش: تقویم هجری شمسی و زمان نسبی

گاهشماری هجری شمسی (جلالی) تقویم رسمی خورشیدی است. ParsiKit الگوریتم‌های دقیق نجومی تبدیل تاریخ را بدون هیچ‌گونه وابستگی جانبی فراهم می‌آورد.

---

## ۱. تبدیل میلادی به هجری شمسی

```python
import parsikit

# تبدیل تاریخ میلادی (سال، ماه، روز)
jy, jm, jd = parsikit.gregorian_to_jalali(2026, 7, 6)
print(f"تاریخ هجری شمسی: {jy}/{jm:02d}/{jd:02d}")
# خروجی: تاریخ هجری شمسی: 1405/04/15

# نام ماه
month_name = parsikit.get_jalali_month_name(jm)
print(f"{jd} {month_name} {jy}")
# خروجی: 15 تیر 1405
```

---

## ۲. تبدیل هجری شمسی به میلادی

```python
import parsikit

gy, gm, gd = parsikit.jalali_to_gregorian(1405, 4, 15)
print(f"تاریخ میلادی: {gy}-{gm:02d}-{gd:02d}")
# خروجی: تاریخ میلادی: 2026-07-06
```

---

## ۳. سنجش سال‌های کبیسه

در گاهشماری هجری شمسی، سال‌های عادی ۳۶۵ روزه و سال‌های کبیسه ۳۶۶ روزه می‌باشند:

```python
import parsikit

print(parsikit.is_jalali_leap(1399))  # True
print(parsikit.is_jalali_leap(1400))  # False
print(parsikit.is_jalali_leap(1403))  # True
print(parsikit.is_jalali_leap(1404))  # False
```

---

## ۴. بیان زمان نسبی به زبان طبیعی

تبدیل اختلاف زمانی ثانیه‌ها یا شیء زمانی به عبارت قابل فهم:

```python
import datetime
import parsikit

# ۵ دقیقه قبل
print(parsikit.humanize_relative_time(-300))
# خروجی: ۵ دقیقه پیش

# ۳ ساعت قبل
print(parsikit.humanize_relative_time(-10800))
# خروجی: ۳ ساعت پیش

# پس‌فردا
print(parsikit.humanize_relative_time(2 * 86400))
# خروجی: پس‌فردا
```
