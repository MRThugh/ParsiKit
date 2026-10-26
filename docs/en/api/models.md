# Domain Models API (`parsikit.models`)

Object-Oriented Domain Models (Value Objects) that perform instant validation upon creation and offer structured attributes, masked representations, comparison operators, and native Pydantic v2 support.
- **Sorting & Comparison**: All models inherit from `StringLikeMixin` with `<, <=, >, >=, ==`, allowing direct sorting (`sorted([card1, card2])`).
- **Resilient Fallbacks (`strict=False`)**: When constructed with `strict=False`, accessing properties such as `.formatted` or `.masked` on malformed inputs safely falls back without raising unhandled exceptions.
- **PII Privacy in Exceptions**: Exception messages mask sensitive middle digits (e.g. `'0912***6789'`, `'IR00****'`) to prevent leaking private data into logs.

---

## 1. `NationalCode(code: str, strict: bool = True)`
- `.is_valid: bool`
- `.formatted: str` (e.g. `'001-012345-8'`)
- `.masked: str` (e.g. `'001-****45-8'`)
- `.location: dict | None` (`{"province": ..., "city": ...}`)
- Raises: `InvalidNationalCodeError`

---

## 2. `MobileNumber(phone: str)`
- `.is_valid: bool`
- `.national: str` (e.g. `'09123456789'`)
- `.international: str` (e.g. `'+989123456789'`)
- `.masked: str` (e.g. `'0912***6789'`)
- `.operator: str | None` (e.g. `'MCI'`)
- Raises: `InvalidMobileError`

---

## 3. `BankCard(card_number: str)`
- `.is_valid: bool`
- `.formatted: str` (e.g. `'6037-9911-2233-4455'`)
- `.masked: str` (e.g. `'6037-99**-****-4455'`)
- `.bank_name: str | None` (e.g. `'بانک ملی ایران'`)
- Raises: `InvalidCardNumberError`

---

## 4. `Sheba(sheba_code: str)`
- `.is_valid: bool`
- `.formatted: str` (e.g. `'IR12 0170 0000 0012 3456 7890 12'`)
- `.bank_name: str | None`
- `.account_number: str`
- Raises: `InvalidShebaError`

---

## 5. `VehiclePlate(plate_text: str)`
- `.is_valid: bool`
- `.formatted: str` (e.g. `'12-B-345-68'`)
- `.category: str` (e.g. `'شخصی'`, `'تاکسی'`)
- `.details: dict`
- Raises: `InvalidPlateError`

---

## 6. `FixedLine(phone: str)`
- `.is_valid: bool`
- `.formatted: str`
- `.province: str | None`
- Raises: `ValidationError`

---

## 7. `PersianText(text: str)`
- `.standardized: str`
- `.stripped: str`
- `.word_count: int`
- `.has_persian: bool`
- `.slug: str`
