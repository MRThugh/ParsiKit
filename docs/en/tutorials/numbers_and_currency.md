# Tutorial: Persian Numbers & Financial Calculations

This tutorial demonstrates script digit conversion, writing numbers in Persian words, currency formatting, and loan calculations.

---

## 1. Digit Script Conversions

Convert numbers between Persian (`۰-۹`), Arabic (`٠-٩`), and English/Latin (`0-9`):

```python
import parsikit

# English to Persian
print(parsikit.english_to_persian("User ID: 1042"))
# 'User ID: ۱۰۴۲'

# Persian/Arabic to English
print(parsikit.persian_to_english("مبلغ: ۲۵۰۰۰ ریال"))
# 'مبلغ: 25000 ریال'
```

---

## 2. Converting Numbers to Written Words

Turn numbers into natural Persian words with high performance (cached):

```python
import parsikit

print(parsikit.number_to_words(0))
# 'صفر'

print(parsikit.number_to_words(1250000))
# 'یک میلیون و دویست و پنجاه هزار'

print(parsikit.number_to_words(-42))
# 'منفی چهل و دو'
```

---

## 3. Currency Transformations (Rial & Toman)

```python
import parsikit

# Rial to Toman (divide by 10)
print(parsikit.rial_to_toman(500000))  # 50000

# Toman to Rial (multiply by 10)
print(parsikit.toman_to_rial(50000))   # 500000

# Formatted currency string
print(parsikit.format_currency(12500000, "toman", persian_digits=True))
# '۱۲،۵۰۰،۰۰۰ تومان'

# Full written currency
print(parsikit.format_currency_to_words(12500000, "toman"))
# 'دوازده میلیون و پانصد هزار تومان'
```

---

## 4. Invoicing & VAT (ارزش افزوده)

Calculate VAT according to the configured tax rate (default: 10%):

```python
import parsikit

invoice = parsikit.add_tax_and_toll(10000000)
print(f"Base: {invoice['original_amount']:,}")
print(f"VAT ({invoice['tax_rate']*100}%): {invoice['tax_amount']:,}")
print(f"Total: {invoice['total_amount']:,}")
```

---

## 5. Loan Installments (محاسبه اقساط)

Calculate monthly installment payments and total interest using the official Central Bank formula:

```python
import parsikit

# 100,000,000 Toman loan at 23% interest for 24 months
loan = parsikit.calculate_installments(100_000_000, 23.0, 24)

print("Monthly installment:", loan['monthly_installment'])
print("Total payment:", loan['total_payment'])
print("Total interest:", loan['total_interest'])
```
