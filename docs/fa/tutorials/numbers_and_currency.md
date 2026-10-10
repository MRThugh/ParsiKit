# آموزش کار با اعداد، مبالغ مالی، تومان و ریال در پارسی‌کیت

یکی از جذاب‌ترین بخش‌های پارسی‌کیت، ابزارهای مالی و تبدیل ارقام و کلمات است.

---

## ۱. تبدیل ارقام انگلیسی، فارسی و عربی

برای تبدیل ارقام در هر دو جهت:

```python
import parsikit

# انگلیسی یا عربی به فارسی
print(parsikit.english_to_persian("Price: 12500 USD"))  # 'Price: ۱۲۵۰۰ USD'

# فارسی یا عربی به انگلیسی
print(parsikit.persian_to_english("قیمت: ۱۲۵۰۰ ریال"))   # 'قیمت: 12500 ریال'

# تابع دوطرفه convert_numbers
print(parsikit.convert_numbers("کد 123", to="persian"))  # 'کد ۱۲۳'
print(parsikit.convert_numbers("کد ۱۲۳", to="english"))  # 'کد 123'
```

---

## ۲. تبدیل عدد به حروف فارسی (`number_to_words`)

پارسی‌کیت از اعداد منفی تا مقادیر نجومی (تا ۹۹۹ سپتیلیون) را به نوشتار سلیس فارسی تبدیل می‌کند:

```python
print(parsikit.number_to_words(0))           # 'صفر'
print(parsikit.number_to_words(14))          # 'چهارده'
print(parsikit.number_to_words(12500))       # 'دوازده هزار و پانصد'
print(parsikit.number_to_words(1500000000))  # 'یک میلیارد و پانصد میلیون'
print(parsikit.number_to_words(-45))         # 'منفی چهل و پنج'
```

---

## ۳. تبدیل حروف فارسی به عدد (`words_to_number`)

کاربر تایپ کرده «سی و دو هزار و پانصد» و می‌خواهی آن را به عدد `32500` در دیتابیس ذخیره کنی:

```python
num = parsikit.words_to_number("سی و دو هزار و پانصد")
print(num)  # 32500

num2 = parsikit.words_to_number("یک میلیون و دویست هزار")
print(num2)  # 1200000

neg = parsikit.words_to_number("منفی پانزده")
print(neg)  # -15
```

---

## ۴. کار با ارزهای تومان و ریال

### تبدیل تومان و ریال
```python
toman = 50000
rial = parsikit.toman_to_rial(toman)
print(rial)  # 500000

back_to_toman = parsikit.rial_to_toman(rial)
print(back_to_toman)  # 50000
```

### فرمت‌بندی مبالغ (`format_currency`)
```python
price = 12500000

# با ارقام انگلیسی و لیبل تومان
print(parsikit.format_currency(price, "toman"))
# '12,500,000 تومان'

# با ارقام و جداکننده هزارگان فارسی (،)
print(parsikit.format_currency(price, "toman", persian_digits=True))
# '۱۲،۵۰۰،۰۰۰ تومان'

# با ریال
print(parsikit.format_currency(parsikit.toman_to_rial(price), "rial", persian_digits=True))
# '۱۲۵،۰۰۰،۰۰۰ ریال'
```

### تبدیل مبلغ به حروف با نام ارز (`format_currency_to_words`)
```python
print(parsikit.format_currency_to_words(1250000, "toman"))
# 'یک میلیون و دویست و پنجاه هزار تومان'
```

---

## ۵. محاسبات مالی (مالیات بر ارزش افزوده و اقساط وام)

### محاسبه مالیات و عوارض (VAT)
به طور پیش‌فرض نرخ مالیات ۱۰٪ در نظر گرفته می‌شود:
```python
total = parsikit.add_tax_and_toll(100000)
print(total)  # 110000

# با نرخ دلخواه (مثلاً ۹٪)
total_custom = parsikit.add_tax_and_toll(100000, tax_rate=0.09)
print(total_custom)  # 109000
```

### محاسبه قسط وام (`calculate_installments`)
فرمول استهلاک استاندارد بانکی برای محاسبه قسط ماهانه:
```python
principal = 100_000_000   # اصل مبلغ وام: ۱۰۰ میلیون تومان
annual_rate = 18.0        # سود سالانه: ۱۸ درصد
months = 12               # مدت بازپرداخت: ۱۲ ماه

installment = parsikit.calculate_installments(principal, annual_rate, months)
print(f"قسط ماهانه: {parsikit.format_currency(installment, 'toman', persian_digits=True)}")
```
