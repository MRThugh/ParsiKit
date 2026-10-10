# ParsiKit Quickstart Guide

Get up and running with ParsiKit in less than 5 minutes.

---

## 1. Text Normalization & Standardization

```python
import parsikit

# Fix Arabic letters and irregular spacing
raw_text = "ي كافيه كتاب ها رو برداري و بري"
clean_text = parsikit.standardize_persian(raw_text)

print(clean_text)
# Output: ی کافیه کتاب‌ها رو برداری و بری
```

---

## 2. Iranian National Code (کد ملی)

```python
import parsikit

code = "0010123458"
nc = parsikit.NationalCode(code)

print(nc.is_valid)   # True
print(nc.formatted)  # '001-012345-8'
print(nc.masked)     # '001-****45-8'
print(nc.location)   # {'province': 'تهران', 'city': 'تهران مرکزی'}
```

---

## 3. Numbers & Currency

```python
import parsikit

amount = 1500000

# Format with Persian digits and separator
formatted = parsikit.format_currency(amount, "toman", persian_digits=True)
print(formatted)
# Output: ۱،۵۰۰،۰۰۰ تومان

# Convert to written words
words = parsikit.number_to_words(amount)
print(f"{words} تومان")
# Output: یک میلیون و پانصد هزار تومان
```

---

## 4. Jalali Astronomical Dates

```python
import parsikit

# Convert Gregorian to Jalali
jy, jm, jd = parsikit.gregorian_to_jalali(2026, 7, 6)
month_name = parsikit.get_jalali_month_name(jm)
print(f"{jd} {month_name} {jy}")
# Output: 15 تیر 1405

# Humanize relative time
print(parsikit.humanize_relative_time(-300))
# Output: ۵ دقیقه پیش
```

---

## 5. Mobile Numbers & Bank Cards

```python
import parsikit

# Mobile number
mobile = parsikit.MobileNumber("09123456789")
print(mobile.international)  # '+989123456789'
print(mobile.operator)       # 'MCI'
print(mobile.masked)         # '0912***6789'

# Bank card
card = parsikit.BankCard("6037991122334455")
print(card.bank_name)        # 'بانک ملی ایران'
print(card.formatted)        # '6037-9911-2233-4455'
print(card.masked)           # '6037-99**-****-4455'
```
