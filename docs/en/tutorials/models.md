# Tutorial: Object-Oriented Domain Models

ParsiKit provides rich domain value objects that wrap raw strings into structured, validated Python objects.

---

## 1. Domain Models Overview

Each model validates input on initialization and raises a structured exception if invalid:

| Model | Target Data | Exception on Invalid Input |
|---|---|---|
| `NationalCode` | Iranian National Code (10 digits) | `InvalidNationalCodeError` |
| `MobileNumber` | Iranian mobile phone numbers | `InvalidMobileError` |
| `FixedLine` | Landline phones with province detection | `ValidationError` |
| `BankCard` | 16-digit debit/credit card numbers | `InvalidCardNumberError` |
| `Sheba` | Iranian IBAN numbers (24 digits + IR) | `InvalidShebaError` |
| `VehiclePlate` | Automobile license plates | `InvalidPlateError` |
| `PersianText` | Rich text with fluent transformations | `ValidationError` |

---

## 2. Using NationalCode

```python
import parsikit

nc = parsikit.NationalCode("0010123458")

# String representation and duck typing
print(str(nc))        # '0010123458'
print(nc.formatted)   # '001-012345-8'
print(nc.masked)      # '001-****45-8' (safe for logs)
print(nc.location)    # {'province': 'تهران', 'city': 'تهران مرکزی'}
```

---

## 3. Using MobileNumber

```python
import parsikit

m = parsikit.MobileNumber("+989123456789")

print(m.national)       # '09123456789'
print(m.international)  # '+989123456789'
print(m.operator)       # 'MCI'
print(m.masked)         # '0912***6789'
```

---

## 4. Using BankCard

```python
import parsikit

card = parsikit.BankCard("6037991122334455")

print(card.bank_name)  # 'بانک ملی ایران'
print(card.formatted)  # '6037-9911-2233-4455'
print(card.masked)     # '6037-99**-****-4455'
```

---

## 5. Native Integration with Pydantic v2 & FastAPI

ParsiKit models implement `__get_pydantic_core_schema__`, allowing them to be used directly as field types in Pydantic schemas:

```python
from pydantic import BaseModel
import parsikit

class UserProfileSchema(BaseModel):
    name: str
    national_code: parsikit.NationalCode
    phone: parsikit.MobileNumber
    card: parsikit.BankCard

# Automatic parsing and validation
profile = UserProfileSchema(
    name="Ali Kamrani",
    national_code="0010123458",
    phone="09123456789",
    card="6037991122334455",
)

print(profile.model_dump())
# All fields serialize cleanly to standard validated strings!
```
