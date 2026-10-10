# آموزش اعتبارسنجی داده‌های هویتی، بانکی و ارتباطی ایران

توی هر سامانه‌ای که توی ایران کار می‌کنه، اعتبارسنجی ورودی‌های کاربر (مثل کد ملی، کارت بانکی، شماره شبا، موبایل و پلاک) پای ثابت توسعه است. پارسی‌کیت الگوریتم‌های رسمی تمام این موارد رو به صورت پیش‌فرض درون خودش داره.

---

## ۱. اعتبارسنجی کد ملی ایران

کد ملی ایران یک رشته ۱۰ رقمیه که رقم دهم، رقم کنترلی حاصل از فرمول پیمانه ۱۱ (Modulo 11) ۹ رقم اوله.

```python
import parsikit

# ۱. اعتبارسنجی ساده (True / False)
print(parsikit.is_valid_national_code("7730123452"))  # True
print(parsikit.is_valid_national_code("1111111111"))  # False (ارقام تکراری نامعتبر است)

# ۲. فرمت‌بندی با خط تیره
print(parsikit.format_national_code("7730123452"))    # '773-012345-2'

# ۳. تشخیص شهر و استان صدور از روی ۳ رقم اول
location = parsikit.detect_national_code_location("0010123458")
print(location)
# {'province': 'تهران', 'city': 'تهران مرکزی'}
```

> **نکته امنیتی:** پارسی‌کیت الگوریتم ریاضی کد ملی را بررسی می‌کند؛ صحت زنده بودن شخص یا تطابق نام و کد ملی نیازمند اتصال به ثبت احوال کشور است.

---

## ۲. شماره موبایل و اپراتورها

پشتیبانی از فرمت‌های مختلف ورودی (`09...`، `+989...`، `00989...` و ارقام فارسی):

```python
# اعتبارسنجی
print(parsikit.is_valid_mobile("09123456789"))     # True
print(parsikit.is_valid_mobile("+98۹۱۲۳۴۵۶۷۸۹"))   # True

# یکسان‌سازی فرمت
print(parsikit.normalize_mobile("09123456789", prefix="0"))    # '09123456789'
print(parsikit.normalize_mobile("09123456789", prefix="+98"))  # '+989123456789'

# تشخیص اپراتور
print(parsikit.detect_mobile_operator("09123456789"))  # 'MCI' (همراه اول)
print(parsikit.detect_mobile_operator("09351234567"))  # 'Irancell' (ایرانسل)
print(parsikit.detect_mobile_operator("09201234567"))  # 'RighTel' (رایتل)
```

---

## ۳. کارت بانکی و تشخیص بانک

بررسی الگوریتم لان (Luhn Checksum) و تفکیک بانک از روی ۶ رقم اول (BIN):

```python
card = "6037991122334455"

print(parsikit.is_valid_card_number(card))  # True
print(parsikit.format_card_number(card))    # '6037-9911-2233-4455'

bank = parsikit.detect_bank_from_card(card)
print(bank)
# {'name': 'بانک ملی ایران', 'code': 'melli'}
```

---

## ۴. شماره شبا (IBAN ایران)

شماره شبا در ایران با ۲ حرف `IR` و سپس ۲۴ رقم تشکیل می‌شود (مجموعاً ۲۶ کاراکتر) و از فرمول Modulo 97 استاندارد بین‌المللی استفاده می‌کند:

```python
sheba = "IR050170000000123456789012"

print(parsikit.is_valid_sheba(sheba))  # True
print(parsikit.format_sheba(sheba, format_type="spaced"))
# 'IR05 0170 0000 0012 3456 7890 12'

# استخراج تمیز شماره حساب داخلی
acc = parsikit.extract_account_number_from_sheba(sheba)
print(acc)  # '123456789012'

# تشخیص بانک صادرکننده شبا
bank = parsikit.detect_bank_from_sheba(sheba)
print(bank)
# {'name': 'بانک ملی ایران', 'code': 'melli'}
```

---

## ۵. پلاک وسایل نقلیه (پلاک ملی)

تجزیه و تحلیل پلاک‌های خودروهای ایران:

```python
plate_text = "۱۲ ب ۳۴۵ ایران ۶۸"

print(parsikit.is_valid_plate(plate_text))  # True

details = parsikit.parse_plate(plate_text)
print(details)
# {
#   'part1': '۱۲',
#   'letter': 'ب',
#   'part2': '۳۴۵',
#   'province_code': '۶۸',
#   'province': 'البرز',
#   'category': 'شخصی'
# }
```

---

## ۶. کد پستی ۱۰ رقمی

```python
postal = "1345678912"
print(parsikit.is_valid_postal_code(postal))  # True
print(parsikit.format_postal_code(postal))    # '13456-78912'
```

---

## ۷. تشخیص خودکار نوع داده (`detect`)

اگر نمی‌دونی متنی که کاربر فرستاده چیه (موبایل، کارت، شبا، ایمیل یا آی‌پی)، تابع `detect` نوع اون رو حدس می‌زنه:

```python
print(parsikit.detect("09123456789"))                  # 'mobile_number'
print(parsikit.detect("6037-9911-2233-4455"))          # 'bank_card'
print(parsikit.detect("IR050170000000123456789012"))   # 'sheba'
print(parsikit.detect("test@example.com"))              # 'email'
print(parsikit.detect("192.168.1.1"))                  # 'ip'
print(parsikit.detect("متن عادی"))                     # None
```
