# Омӯзиш: Моделҳои объекти нигаронидашуда (Domain Models)

Китобхонаи ParsiKit моделҳои сохторёфтаи арзишманд (Value Objects) пешниҳод мекунад, ки сатрҳои хомро ба объектҳои санҷидашуда табдил медиҳанд.

---

## 1. Назари умумӣ ба моделҳо

Ҳар як модел ҳангоми сохта шудан маълумотро месанҷад ва дар сурати нодурустӣ истиснои мушаххас медиҳад:

| Модел | Навъи маълумот | Истисно дар сурати нодурустӣ |
|---|---|---|
| `NationalCode` | Рамзи миллии 10-рақама | `InvalidNationalCodeError` |
| `MobileNumber` | Рақами телефони мобилӣ | `InvalidMobileError` |
| `FixedLine` | Телефони доимӣ бо шинохти шаҳр | `ValidationError` |
| `BankCard` | Корти бонкии 16-рақама | `InvalidCardNumberError` |
| `Sheba` | Суратҳисоби бонкӣ (IBAN) | `InvalidShebaError` |
| `VehiclePlate` | Рақами қайди давлатии нақлиёт | `InvalidPlateError` |
| `PersianText` | Матн бо методҳои занҷирӣ | `ValidationError` |

---

## 2. Истифода аз `NationalCode`

```python
import parsikit

nc = parsikit.NationalCode("0010123458")

print(str(nc))        # '0010123458'
print(nc.formatted)   # '001-012345-8'
print(nc.masked)      # '001-****45-8' (барои логҳо)
print(nc.location)    # {'province': 'تهران', 'city': 'تهران مرکزی'}
```

---

## 3. Истифода аз `MobileNumber`

```python
import parsikit

m = parsikit.MobileNumber("+989123456789")

print(m.national)       # '09123456789'
print(m.international)  # '+989123456789'
print(m.operator)       # 'MCI'
print(m.masked)         # '0912***6789'
```

---

## 4. Истифода аз `BankCard`

```python
import parsikit

card = parsikit.BankCard("6037991122334455")

print(card.bank_name)  # 'بانک ملی ایران'
print(card.formatted)  # '6037-9911-2233-4455'
print(card.masked)     # '6037-99**-****-4455'
```

---

## 5. Ҳамоҳангӣ бо Pydantic v2 ва FastAPI

Моделҳо протоколи `__get_pydantic_core_schema__`-ро татбиқ намудаанд:

```python
from pydantic import BaseModel
import parsikit

class UserProfileSchema(BaseModel):
    name: str
    national_code: parsikit.NationalCode
    phone: parsikit.MobileNumber
    card: parsikit.BankCard

profile = UserProfileSchema(
    name="Рустам",
    national_code="0010123458",
    phone="09123456789",
    card="6037991122334455",
)

print(profile.model_dump())
```
