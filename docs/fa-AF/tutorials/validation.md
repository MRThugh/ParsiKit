# آموزش: اعتبارسنجی شناسه‌ها و ساختارهای رسمی

موتورهای اعتبارسنجی ParsiKit برای تصدیق ساختار انواع شناسه‌ها و اسناد:

---

## ۱. کود شناسایی ملی (کد ملی)

کود ملی یک شماره‌ی ۱۰ رقمی است که رقم دهم آن حاصل فرمول چک‌سام مبنای ۱۱ با ضرایب وزنی ۱۰ تا ۲ می‌باشد:

```python
import parsikit

# اعتبارسنجی
print(parsikit.is_valid_national_code("0010123458"))  # True
print(parsikit.is_valid_national_code("1111111111"))  # False (ارقام تکراری)
print(parsikit.is_valid_national_code("0010123451"))  # False (چک‌سام نادرست)

# قالب‌بندی
print(parsikit.format_national_code("0010123458"))    # '001-012345-8'

# تشخیص محل صدور
print(parsikit.detect_national_code_location("0010123458"))
# {'province': 'تهران', 'city': 'تهران مرکزی'}
```

---

## ۲. شماره‌های مبایل

```python
import parsikit

phone = "+989123456789"
print(parsikit.is_valid_mobile(phone))           # True
print(parsikit.normalize_mobile(phone, "0"))     # '09123456789'
print(parsikit.detect_mobile_operator(phone))    # 'MCI'
```

---

## ۳. کارت‌های بانکی و شماره‌ی شبا

### کارت‌های ۱۶ رقمی
بررسی الگوریتم لان (Luhn) و شناسایی بانک صادرکننده:

```python
import parsikit

card = "6037991122334455"
print(parsikit.is_valid_card_number(card))       # True
print(parsikit.format_card_number(card))         # '6037-9911-2233-4455'
print(parsikit.detect_bank_from_card(card))      # 'بانک ملی ایران'
```

### شماره‌ی شبا (IBAN)
بررسی ۲۴ رقم بر اساس ISO 7064 Mod 97-10:

```python
import parsikit

sheba = "IR120170000000123456789012"
print(parsikit.is_valid_sheba(sheba))             # True
print(parsikit.detect_bank_from_sheba(sheba))     # 'بانک ملی ایران'
```

---

## ۴. کود پستی و قبوض خدماتی

```python
import parsikit

# کود پستی ۱۰ رقمی
print(parsikit.is_valid_postal_code("1417466191"))  # True
print(parsikit.format_postal_code("1417466191"))    # '14174-66191'

# شناسه‌ی قبض و پرداخت
bill_id = "982765410123"
pay_id = "12500345"
```
