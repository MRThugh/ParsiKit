# آموزش مدل‌های شیءگرا در پارسی‌کیت (Domain Models)

در کنار توابع مستقل، پارسی‌کیت مجموعه‌ای از کلاس‌های غنی شیءگرا (OOP Domain Models) در ماژول `parsikit.models` فراهم کرده تا توسعه‌دهنده‌ها بتونن با موجودیت‌های دیتایی به راحتی کار کنند.

---

## ویژگی‌های مشترک تمام مدل‌ها

همه مدل‌های پارسی‌کیت از دو Mixin قدرتمند ارث‌بری می‌کنند:
1. **`StringLikeMixin` (شبه‌رشته):**  
   می‌تونی با شیء درست مثل یک رشته پایتون رفتار کنی (`len(obj)`، برش با اسلایس `obj[:3]`، چک کردن برابری با استرینگ `obj == "..."` و استفاده به عنوان کلید دیکشنری).
2. **`PydanticValidationMixin`:**  
   بدون هیچ کار اضافی، می‌تونی از این مدل‌ها به عنوان نوع فیلد در اسکیماهای Pydantic v2 (مثلاً در FastAPI) استفاده کنی.
3. **متد `to_dict()`:**  
   تمام اطلاعات و فراداده‌های مدل را به صورت یک دیکشنری ساخت‌یافته خروجی می‌دهد.

---

## ۱. مدل متن فارسی (`PersianText`)

یک رشته متن فارسی که متدهای زنجیره‌ای (Chained Methods) برای پاک‌سازی روی خودش دارد:

```python
import parsikit

text = parsikit.PersianText("ي كافيه كتاب ها رو برداري")
clean = text.standardize().beautify()
print(clean)
# 'ی کافیه کتاب‌ها رو برداری'

# اتصال به رشته‌های دیگر
combined = text + " و جهان"
print(type(combined))  # <class 'parsikit.models.PersianText'>

# تبدیل متن عددی به عدد
price_text = parsikit.PersianText("سه میلیارد و پانصد میلیون")
print(price_text.to_number())  # 3500000000
```

---

## ۲. مدل کد ملی (`NationalCode`)

```python
import parsikit

# ساخت شیء با اعتبارسنجی پیش‌فرض (strict=True)
nc = parsikit.NationalCode("7730123452")

print(nc.clean)      # '7730123452'
print(nc.formatted)  # '773-012345-2'
print(nc.masked)     # '773-****45-2'
print(nc.is_valid)   # True
print(len(nc))       # 10
print(nc.location)   # {'province': 'فارس', 'city': ...}

# رفتار دقیقاً شبیه رشته پایتون
print(nc == "7730123452")  # True

# خروجی دیکشنری
print(nc.to_dict())
```

اگر کد ملی نامعتبر باشد و `strict=True` باشد، خطای `InvalidNationalCodeError` پرتاب می‌شود. با `strict=False` می‌توانید خطای اعتبارسنجی را بدون Exception ثبت کنید:
```python
nc_loose = parsikit.NationalCode("1111111111", strict=False)
print(nc_loose.is_valid)  # False
```

---

## ۳. مدل شماره موبایل (`MobileNumber`)

```python
mob = parsikit.MobileNumber("+98۹۱۲۳۴۵۶۷۸۹")

print(mob.to_national())       # '09123456789'
print(mob.to_international())  # '+989123456789'
print(mob.operator)            # 'MCI'
print(mob.masked)              # '0912***6789'
```

---

## ۴. مدل تلفن ثابت (`FixedLine`)

```python
fixed = parsikit.FixedLine("02188888888")

print(fixed.province)   # 'تهران'
print(fixed.area_code)  # '021'
print(fixed.to_national())  # '02188888888'
```

---

## ۵. مدل کارت بانکی (`BankCard`)

```python
card = parsikit.BankCard("6037991122334455")

print(card.formatted)  # '6037-9911-2233-4455'
print(card.masked)     # '6037-99**-****-4455'
print(card.bank)       # {'name': 'بانک ملی ایران', 'code': 'melli'}
```

---

## ۶. مدل شبا (`Sheba`)

```python
sheba = parsikit.Sheba("IR050170000000123456789012")

print(sheba.formatted)       # 'IR05 0170 0000 0012 3456 7890 12'
print(sheba.bank)            # {'name': 'بانک ملی ایران', 'code': 'melli'}
print(sheba.account_number)  # '123456789012'
```

---

## ۷. مدل پلاک ملی خودرو (`VehiclePlate`)

```python
plate = parsikit.VehiclePlate("۱۲ ب ۳۴۵ ایران ۶۸")

print(plate.province)       # 'البرز'
print(plate.province_code)  # '۶۸'
print(plate.category)       # 'شخصی'
print(plate.formatted)      # '۱۲ ب ۳۴۵ - ایران ۶۸'
```
