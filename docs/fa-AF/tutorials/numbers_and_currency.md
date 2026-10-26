# آموزش: ارقام و محاسبات مالی در پایتون

این آموزش نحوه‌ی تبدیل خط ارقام، تبدیل عدد به حروف، قالب‌بندی مبالغ و سنجش مالیات و اقساط را نشان می‌دهد.

---

## ۱. تبدیل خط ارقام

تبدیل میان ارقام فارسی (`۰-۹`)، عربی (`٠-٩`) و انگلیسی (`0-9`):

```python
import parsikit

# انگلیسی به فارسی
print(parsikit.english_to_persian("آیدی کاربر: 1042"))
# 'آیدی کاربر: ۱۰۴۲'

# فارسی/عربی به انگلیسی
print(parsikit.persian_to_english("مبلغ: ۲۵۰۰۰ ریال"))
# 'مبلغ: 25000 ریال'
```

---

## ۲. تبدیل اعداد به حروف نوشتاری

تبدیل سریع اعداد بزرگ به حروف با بهره‌گیری از کش داخلی:

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

## ۳. تبدیلات پولی (ریال و تومان)

```python
import parsikit

# ریال به تومان (تقسیم بر ۱۰)
print(parsikit.rial_to_toman(500000))  # 50000

# تومان به ریال (ضرب در ۱۰)
print(parsikit.toman_to_rial(50000))   # 500000

# قالب‌بندی با جداکننده‌ی سه‌رقمی
print(parsikit.format_currency(12500000, "toman", persian_digits=True))
# '۱۲،۵۰۰،۰۰۰ تومان'

# نوشتن مبلغ به حروف
print(parsikit.format_currency_to_words(12500000, "toman"))
# 'دوازده میلیون و پانصد هزار تومان'
```

---

## ۴. محاسبه‌ی مالیات بر ارزش افزوده

محاسبه‌ی مالیات مطابق با نرخ تنظیم‌شده (پیش‌فرض: ۱۰٪):

```python
import parsikit

invoice = parsikit.add_tax_and_toll(10000000)
print(f"مبلغ پایه: {invoice['original_amount']:,}")
print(f"مالیات ({invoice['tax_rate']*100}%): {invoice['tax_amount']:,}")
print(f"مجموع قابل پرداخت: {invoice['total_amount']:,}")
```

---

## ۵. محاسبه‌ی اقساط ماهوار وام (Installments)

```python
import parsikit

# تسهیلات ۱۰۰ میلیون با سود سالانه‌ی ۲۳٪ برای مدت ۲۴ ماه
loan = parsikit.calculate_installments(100_000_000, 23.0, 24)

print("قسط ماهانه:", loan['monthly_installment'])
print("مجموع بازپرداخت:", loan['total_payment'])
print("مفاد کل:", loan['total_interest'])
```
