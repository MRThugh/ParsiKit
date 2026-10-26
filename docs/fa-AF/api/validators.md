# مرجع ماژول اعتبارسنجی (`parsikit.validators`)

مجموعه توابع سنجش و اعتبارسنجی صحت داده‌های رسمی و مالی:

---

## توابع اعتبارسنجی

### `is_valid_national_code(code: str, strict: bool = True) -> bool`
اعتبارسنجی شناسه ۱۰ رقمی با استفاده از فرمول رسمی باقیمانده‌ی تقسیم بر ۱۱ (چک‌سام).

### `format_national_code(code: str) -> str`
قالب‌بندی شناسه ملی به صورت ۳ بخش خط‌فاصله‌دار (`XXX-XXXXXX-X`).

### `detect_national_code_location(code: str) -> dict | None`
تشخیص ولایت و شهر محل صدور بر بنیاد ۳ رقم ابتدایی.

### `is_valid_mobile(phone: str) -> bool`
اعتبارسنجی ساختار شماره‌ی مبایل بر اساس پیش‌شماره‌های اپراتورها.

### `normalize_mobile(phone: str, prefix: str = "0") -> str`
معیارسازی شماره به قالب محلی (`09...`) یا بین‌المللی (`+989...`).

### `detect_mobile_operator(phone: str) -> str | None`
شناسایی نام شرکت ارائه‌دهنده‌ی خدمات مخابراتی (اپراتور).

### `is_valid_landline(phone: str) -> bool`
اعتبارسنجی شماره‌های تلفون ثابت با پیش‌شماره‌های ولایتی.

### `detect_landline_province(phone: str) -> str | None`
تشخیص ولایت شماره تلفون ثابت.

### `is_valid_card_number(card: str) -> bool`
اعتبارسنجی کارت‌های بانکی ۱۶ رقمی با الگوریتم لان (Luhn Mod-10).

### `format_card_number(card: str, separator: str = "-") -> str`
گروه‌بندی کارت به ۴ بخش چهارتایی مجزا.

### `detect_bank_from_card(card: str) -> str | None`
تشخیص نام بانک صادرکننده‌ی کارت از روی ۶ رقم اول.

### `is_valid_sheba(sheba: str) -> bool`
اعتبارسنجی شماره‌ی شبا (IBAN) بر مبنای استاندارد بین‌المللی ISO 7064 Mod 97-10.

### `format_sheba(sheba: str, chunk_size: int = 4) -> str`
فاصله‌گذاری خوانا در شماره‌ی شبا.

### `detect_bank_from_sheba(sheba: str) -> str | None`
تشخیص نام بانک از روی کود شناسایی موجود در شبا.

### `is_valid_postal_code(code: str) -> bool`
اعتبارسنجی ساختار ۱۰ رقمی کود پستی.

### `format_postal_code(code: str) -> str`
قالب‌بندی کود پستی به شکل دو بخش پنج‌رقمی (`XXXXX-XXXXX`).

### `is_valid_corporate_id(corp_id: str) -> bool`
اعتبارسنجی شناسه ۱۱ رقمی اشخاص حقوقی و شرکت‌ها.

### `is_valid_bill_and_payment(bill_id: str, pay_id: str) -> bool`
اعتبارسنجی شناسه قبض و شناسه پرداخت.

### `extract_bill_details(bill_id: str, pay_id: str) -> dict`
استخراج نوعیت خدمت، مبلغ قابل پرداخت و دوره‌ی صورتحساب.

### `is_valid_plate(plate: str) -> bool`
اعتبارسنجی ساختار نمبر پلیت وسایط نقلیه.

### `parse_plate(plate: str) -> dict`
تحلیل ارقام، حرف میانی و کود ولایت نمبر پلیت.

### `detect(text: str) -> str | None`
تشخیص خودکار و هوشمند نوع داده‌ی ورودی (`national_code`, `mobile`, `card`, `sheba`, `email`, `url`, `ip`).
