# مرجع مدل‌های شیءگرا (`parsikit.models`)

ماژول `parsikit.models` اشیای دامنه (Domain Value Objects) را به روش شیءگرای ناب پیاده‌سازی می‌کند. تمام این مدل‌ها ویژگی‌های زیر را دارا هستند:
- اعتبارسنجی خودکار در هنگام ساخت شیء (Instant Validation).
- پرتاب استثنای مشخص با ماسک خودکار داده‌های حساس در متن پیام خطا.
- پشتیبانی از عملگرهای مقایسه (`<`, `<=`, `>`, `>=`) و امکان مرتب‌سازی مستقیم با `sorted()`.
- حالت منعطف `strict=False` با بازگشت امن مقادیر در ویژگی‌های `.formatted` و `.masked` بدون کرش.
- سازگاری کامل با Pydantic v2 و FastAPI جهت استفاده در فیلدهای Schema.
- محافظت از اطلاعات حساس با صفت `.masked`.

---

## ۱. مدل `PersianText`
مدل کپسوله‌کننده متن فارسی با عملگرهای پردازشی زنجیره‌ای:
```python
from parsikit import PersianText

text = PersianText("  متن نمونه با ارقام ۱۲۳ و كتاب ها  ")
print(text.standardized)    # متن استاندارد با نیم‌فاصله
print(text.word_count)      # تعداد کلمات
print(text.has_persian)     # True
print(text.slug)            # اسلاگ سئو فینگلیش
```

---

## ۲. مدل `NationalCode`
مدل کپسوله‌کننده کد ملی ایران:
```python
from parsikit import NationalCode

nc = NationalCode("0010123458")
print(nc.formatted)         # '001-012345-8'
print(nc.masked)            # '001-****45-8' (ایمن برای لاگ‌ها)
print(nc.location)          # {'province': 'تهران', 'city': 'تهران مرکزی'}
print(nc.is_valid)          # True
```

---

## ۳. مدل `MobileNumber`
مدل شماره تلفن همراه ایران:
```python
from parsikit import MobileNumber

m = MobileNumber("+989123456789")
print(m.national)           # '09123456789'
print(m.international)      # '+989123456789'
print(m.masked)             # '0912***6789'
print(m.operator)           # 'MCI'
```

---

## ۴. مدل `BankCard`
مدل شماره کارت بانکی ۱۶ رقمی شتاب:
```python
from parsikit import BankCard

card = BankCard("6037991122334455")
print(card.formatted)       # '6037-9911-2233-4455'
print(card.masked)          # '6037-99**-****-4455'
print(card.bank_name)       # 'بانک ملی ایران'
```

---

## ۵. مدل `Sheba`
مدل شماره شبای بانکی ایران:
```python
from parsikit import Sheba

s = Sheba("IR120170000000123456789012")
print(s.formatted)          # 'IR12 0170 0000 0012 3456 7890 12'
print(s.bank_name)          # 'بانک ملی ایران'
print(s.account_number)     # شماره حساب پالایش‌شده درونی
```

---

## ۶. مدل `VehiclePlate`
مدل پلاک خودروی ایرانی:
```python
from parsikit import VehiclePlate

p = VehiclePlate("۱۲ ب ۳۴۵ ایران ۶۸")
print(p.formatted)          # '12-B-345-68'
print(p.category)           # 'شخصی' (یا 'تاکسی', 'عمومی')
print(p.details)            # اطلاعات تفکیک‌شده پلاک
```
