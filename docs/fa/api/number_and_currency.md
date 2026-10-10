# مرجع توابع اعداد و محاسبات ارزی (`parsikit.number`, `parsikit.currency`)

این ماژول‌ها امکان تبدیل ارقام، نوشتن اعداد به حروف، تبدیل واحدهای ریال و تومان، مالیات ارزش افزوده و محاسبات بانکی را در اختیار قرار می‌دهند.

---

## ۱. تبدیل ارقام و عدد به حروف (`parsikit.number`)

### `english_to_persian(text: str) -> str`
تمامی ارقام انگلیسی موجود در متن (`0-9`) را به ارقام متناظر فارسی (`۰-۹`) تبدیل می‌کند.

### `persian_to_english(text: str) -> str`
ارقام فارسی (`۰-۹`) و عربی (`٠-٩`) را به ارقام استاندارد انگلیسی (`0-9`) تبدیل می‌نماید.

### `number_to_words(number: int | float) -> str`
اعداد بزرگ (تا مقیاس سپتیلیون) را به نوشتار حروفی فارسی برمی‌گرداند. مجهز به سیستم کش LRU داخلی برای بیشترین کارایی.

```python
import parsikit

print(parsikit.number_to_words(1250000))
# 'یک میلیون و دویست و پنجاه هزار'
```

---

## ۲. امور مالی و واحدهای پولی (`parsikit.currency`)

### `rial_to_toman(amount: int | float) -> int | float`
مبلغ را از ریال به تومان تقسیم بر ۱۰ تبدیل می‌کند.

### `toman_to_rial(amount: int | float) -> int | float`
مبلغ را از تومان به ریال ضربدر ۱۰ تبدیل می‌کند.

### `format_currency(amount, currency="toman", *, persian_digits=False) -> str`
مبلغ را با جداساز سه‌رقمی هزارگان (با ویرگول فارسی یا انگلیسی) و پسوند واحد پولی قالب‌بندی می‌کند.

```python
print(parsikit.format_currency(1500000, "toman", persian_digits=True))
# '۱،۵۰۰،۰۰۰ تومان'
```

### `format_currency_to_words(amount, currency="toman") -> str`
مبلغ عددی را همراه با نام واحد پول به صورت حروفی کامل توصیف می‌کند.

### `add_tax_and_toll(amount, tax_rate=None) -> dict`
مبلغ مالیات بر ارزش افزوده و مبلغ نهایی فاکتور را محاسبه می‌کند:
```python
inv = parsikit.add_tax_and_toll(10000000)
print(inv)
# {'original_amount': 10000000, 'tax_rate': 0.1, 'tax_amount': 1000000.0, 'total_amount': 11000000.0}
```

### `calculate_installments(principal, annual_interest_rate, months) -> dict`
محاسبه اقساط ماهانه تسهیلات بانکی، سود کل و مجموع بازپرداخت بر اساس فرمول بانک مرکزی.
