# Маълумотномаи моделҳои объекти нигаронидашуда (`parsikit.models`)

Моделҳои сохторёфтаи маълумотӣ (Value Objects), ки ҳангоми сохта шудан маълумотро санҷида, хусусиятҳои иловагиро дастрас мегардонанд:

---

## 1. `NationalCode(code: str, strict: bool = True)`
- `.is_valid: bool`
- `.formatted: str` (қолаби стандартӣ: `'001-012345-8'`)
- `.masked: str` (ниқобпӯшшуда: `'001-****45-8'`)
- `.location: dict | None` (`{"province": ..., "city": ...}`)
- Истисно: `InvalidNationalCodeError`

---

## 2. `MobileNumber(phone: str)`
- `.is_valid: bool`
- `.national: str` (масалан: `'09123456789'`)
- `.international: str` (масалан: `'+989123456789'`)
- `.masked: str` (масалан: `'0912***6789'`)
- `.operator: str | None` (номи ширкати мобилӣ, масалан: `'MCI'`)
- Истисно: `InvalidMobileError`

---

## 3. `BankCard(card_number: str)`
- `.is_valid: bool`
- `.formatted: str` (чор рақамӣ бо хатча: `'6037-9911-2233-4455'`)
- `.masked: str` (масалан: `'6037-99**-****-4455'`)
- `.bank_name: str | None` (номи бонки содиркунанда)
- Истисно: `InvalidCardNumberError`

---

## 4. `Sheba(sheba_code: str)`
- `.is_valid: bool`
- `.formatted: str` (қолаби фосиладор бо 4 рамз)
- `.bank_name: str | None`
- `.account_number: str`
- Истисно: `InvalidShebaError`

---

## 5. `VehiclePlate(plate_text: str)`
- `.is_valid: bool`
- `.formatted: str`
- `.category: str` (шахсӣ, таксӣ, давлатӣ)
- `.details: dict`
- Истисно: `InvalidPlateError`

---

## 6. `FixedLine(phone: str)`
- `.is_valid: bool`
- `.formatted: str`
- `.province: str | None`
- Истисно: `ValidationError`

---

## 7. `PersianText(text: str)`
- `.standardized: str`
- `.stripped: str`
- `.word_count: int`
- `.has_persian: bool`
- `.slug: str`
