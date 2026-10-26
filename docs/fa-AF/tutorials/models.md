# آموزش: مودل‌های دامنه‌ی شی‌گرا (Domain Models)

کتابخانه‌ی ParsiKit مودل‌های غنی ارزش‌محور (Value Objects) ارائه می‌کند که رشته‌های خام ورودی را درون شیءهای تصدیق‌شده قرار می‌دهند.

---

## ۱. نگاه کلی به مودل‌های دامنه

هر مودل هنگام نمونه‌سازی، داده‌ی ورودی را اعتبارسنجی می‌کند و در صورت نادرست بودن، استثنای مشخصی پرتاب می‌نماید:

| مودل | نوع داده‌ی هدف | استثنا در صورت نامعتبر بودن |
|---|---|---|
| `NationalCode` | شناسه / کود ملی (۱۰ رقمی) | `InvalidNationalCodeError` |
| `MobileNumber` | شماره تلفون مبایل | `InvalidMobileError` |
| `FixedLine` | تلفون ثابت و تشخیص ولایت | `ValidationError` |
| `BankCard` | کارت بانکی ۱۶ رقمی | `InvalidCardNumberError` |
| `Sheba` | شماره شبا / IBAN | `InvalidShebaError` |
| `VehiclePlate` | نمبر پلیت وسایط نقلیه | `InvalidPlateError` |
| `PersianText` | متن غنی با متدهای زنجیره‌ای | `ValidationError` |

---

## ۲. استفاده از `NationalCode`

```python
import parsikit

nc = parsikit.NationalCode("0010123458")

print(str(nc))        # '0010123458'
print(nc.formatted)   # '001-012345-8'
print(nc.masked)      # '001-****45-8' (مناسب برای ثبت در لاگ‌ها)
print(nc.location)    # {'province': 'تهران', 'city': 'تهران مرکزی'}
```

---

## ۳. استفاده از `MobileNumber`

```python
import parsikit

m = parsikit.MobileNumber("+989123456789")

print(m.national)       # '09123456789'
print(m.international)  # '+989123456789'
print(m.operator)       # 'MCI'
print(m.masked)         # '0912***6789'
```

---

## ۴. استفاده از `BankCard`

```python
import parsikit

card = parsikit.BankCard("6037991122334455")

print(card.bank_name)  # 'بانک ملی ایران'
print(card.formatted)  # '6037-9911-2233-4455'
print(card.masked)     # '6037-99**-****-4455'
```

---

## ۵. هماهنگی مستقیم با Pydantic v2 و FastAPI

مودل‌ها متد پروتکل `__get_pydantic_core_schema__` را تطبیق داده‌اند:

```python
from pydantic import BaseModel
import parsikit

class UserProfileSchema(BaseModel):
    name: str
    national_code: parsikit.NationalCode
    phone: parsikit.MobileNumber
    card: parsikit.BankCard

profile = UserProfileSchema(
    name="احمد",
    national_code="0010123458",
    phone="09123456789",
    card="6037991122334455",
)

print(profile.model_dump())
```
