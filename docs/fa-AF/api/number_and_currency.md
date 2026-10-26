# مرجع ماژول‌های ارقام و محاسبات مالی (`parsikit.number`, `parsikit.currency`)

---

## ارقام (`parsikit.number`)

### `english_to_persian(text: str) -> str`
تبدیل ارقام انگلیسی (`0-9`) به ارقام فارسی (`۰-۹`).

### `persian_to_english(text: str) -> str`
تبدیل ارقام فارسی و عربی به ارقام اسکی انگلیسی (`0-9`).

### `number_to_words(number: int | float) -> str`
تبدیل اعداد به حروف نوشتاری تا سقف سپتیلیون با بهره‌گیری از کش پرشتاب.

---

## محاسبات مالی (`parsikit.currency`)

### `rial_to_toman(amount: int | float) -> int | float`
تبدیل ریال به تومان (تقسیم بر ۱۰).

### `toman_to_rial(amount: int | float) -> int | float`
تبدیل تومان به ریال (ضرب در ۱۰).

### `format_currency(amount, currency="toman", *, persian_digits=False) -> str`
قالب‌بندی مبالغ با جداکننده‌ی ۳رقمی هزارگان و درج واحد پولی.

### `format_currency_to_words(amount, currency="toman") -> str`
نوشتن مبلغ پولی به حروف همراه با پسوند واحد پولی.

### `add_tax_and_toll(amount, tax_rate=None) -> dict`
محاسبه‌ی مالیات بر ارزش افزوده و سنجش مبلغ نهایی فاکتور.

### `calculate_installments(principal, annual_interest_rate, months) -> dict`
محاسبه‌ی اقساط ماهوار، مفاد کل و مجموع بازپرداخت بر بنیاد فرمول معیاری بانکی.
