# Tutorial: Jalali (Solar Hijri) Dates & Relative Time

The Jalali calendar is the official solar astronomical calendar used in Iran and Afghanistan. ParsiKit provides pure-Python astronomical conversion algorithms with zero dependencies.

---

## 1. Gregorian to Jalali Conversion

```python
import parsikit

# Convert Gregorian date (Year, Month, Day)
jy, jm, jd = parsikit.gregorian_to_jalali(2026, 7, 6)
print(f"Jalali date: {jy}/{jm:02d}/{jd:02d}")
# Output: Jalali date: 1405/04/15

# Persian month name
month_name = parsikit.get_jalali_month_name(jm)
print(f"{jd} {month_name} {jy}")
# Output: 15 تیر 1405
```

---

## 2. Jalali to Gregorian Conversion

```python
import parsikit

# Convert Jalali date back to Gregorian
gy, gm, gd = parsikit.jalali_to_gregorian(1405, 4, 15)
print(f"Gregorian date: {gy}-{gm:02d}-{gd:02d}")
# Output: Gregorian date: 2026-07-06
```

---

## 3. Jalali Leap Years (سال کبیسه)

In the Jalali calendar, a normal year has 365 days (months 1-6 have 31 days, 7-11 have 30 days, and month 12 has 29 days). A leap year has 366 days, with month 12 (Esfand) having 30 days.

```python
import parsikit

# Check astronomical leap years
print(parsikit.is_jalali_leap(1399))  # True
print(parsikit.is_jalali_leap(1400))  # False
print(parsikit.is_jalali_leap(1403))  # True
print(parsikit.is_jalali_leap(1404))  # False
```

---

## 4. Humanized Relative Time

Turn timestamps or second offsets into natural Persian strings:

```python
import datetime
import parsikit

now = datetime.datetime.now()

# 5 minutes ago
print(parsikit.humanize_relative_time(-300))
# Output: ۵ دقیقه پیش

# 3 hours ago
print(parsikit.humanize_relative_time(-10800))
# Output: ۴ ساعت پیش

# In 2 days
print(parsikit.humanize_relative_time(2 * 86400))
# Output: پس‌فردا
```
