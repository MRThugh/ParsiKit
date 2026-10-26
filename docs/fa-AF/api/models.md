# مرجع مودل‌های شی‌گرا (`parsikit.models`)

مودل‌های دامنه‌ی شی‌گرا (Value Objects) که به محض ساخت نمونه، ورودی را اعتبارسنجی کرده و خصوصیات مفیدی را استخراج می‌نمایند:

---

## ۱. `NationalCode(code: str, strict: bool = True)`
- `.is_valid: bool`
- `.formatted: str` (قالب استاندارد: `'001-012345-8'`)
- `.masked: str` (ماسک‌شده: `'001-****45-8'`)
- `.location: dict | None` (`{"province": ..., "city": ...}`)
- استثنای نامعتبر بودن: `InvalidNationalCodeError`

---

## ۲. `MobileNumber(phone: str)`
- `.is_valid: bool`
- `.national: str` (مثال: `'09123456789'`)
- `.international: str` (مثال: `'+989123456789'`)
- `.masked: str` (مثال: `'0912***6789'`)
- `.operator: str | None` (شناسایی اپراتور، مثال: `'MCI'`)
- استثنای نامعتبر بودن: `InvalidMobileError`

---

## ۳. `BankCard(card_number: str)`
- `.is_valid: bool`
- `.formatted: str` (چهار رقم چهار رقم: `'6037-9911-2233-4455'`)
- `.masked: str` (مثال: `'6037-99**-****-4455'`)
- `.bank_name: str | None` (تشخیص بانک صادرکننده)
- استثنای نامعتبر بودن: `InvalidCardNumberError`

---

## ۴. `Sheba(sheba_code: str)`
- `.is_valid: bool`
- `.formatted: str` (قالب دسته‌بندی‌شده با فاصله)
- `.bank_name: str | None`
- `.account_number: str`
- استثنای نامعتبر بودن: `InvalidShebaError`

---

## ۵. `VehiclePlate(plate_text: str)`
- `.is_valid: bool`
- `.formatted: str`
- `.category: str` (شخصی، تاکسی، دولتی و...)
- `.details: dict`
- استثنای نامعتبر بودن: `InvalidPlateError`

---

## ۶. `FixedLine(phone: str)`
- `.is_valid: bool`
- `.formatted: str`
- `.province: str | None`
- استثنای نامعتبر بودن: `ValidationError`

---

## ۷. `PersianText(text: str)`
- `.standardized: str`
- `.stripped: str`
- `.word_count: int`
- `.has_persian: bool`
- `.slug: str`
