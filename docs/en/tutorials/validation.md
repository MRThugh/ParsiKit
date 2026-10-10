# Tutorial: National Identifiers & Format Validation

ParsiKit provides validation engines for all major Iranian public identification standards.

---

## 1. Iranian National Code (کد ملی)

The Iranian National Code is a 10-digit number where the 10th digit is a checksum computed modulo 11 with weights from 10 down to 2.

```python
import parsikit

# Verification
print(parsikit.is_valid_national_code("0010123458"))  # True
print(parsikit.is_valid_national_code("1111111111"))  # False (repeated digits)
print(parsikit.is_valid_national_code("0010123451"))  # False (invalid checksum)

# Formatting
print(parsikit.format_national_code("0010123458"))    # '001-012345-8'

# Origin detection
print(parsikit.detect_national_code_location("0010123458"))
# {'province': 'تهران', 'city': 'تهران مرکزی'}
```

---

## 2. Iranian Mobile Numbers (شماره موبایل)

Supports standard 11-digit Iranian mobile numbers across MCI (Hamrah-e Aval), Irancell (MTN), Rightel, Shatel Mobile, and enterprise virtual operators:

```python
import parsikit

phone = "+989123456789"
print(parsikit.is_valid_mobile(phone))           # True
print(parsikit.normalize_mobile(phone, "0"))     # '09123456789'
print(parsikit.detect_mobile_operator(phone))    # 'MCI'
```

---

## 3. Bank Cards & Sheba IBANs

### 16-Digit Debit Cards (کارت بانکی شتاب)
Uses the Luhn algorithm (mod-10 double-add-double) and matches issuer bank codes:

```python
import parsikit

card = "6037991122334455"
print(parsikit.is_valid_card_number(card))       # True
print(parsikit.format_card_number(card))         # '6037-9911-2233-4455'
print(parsikit.detect_bank_from_card(card))      # 'بانک ملی ایران'
```

### Sheba (شناسه بانکی ایران - IBAN)
Evaluates 24-digit Iranian IBAN numbers according to ISO 7064 Mod 97-10:

```python
import parsikit

sheba = "IR120170000000123456789012"
print(parsikit.is_valid_sheba(sheba))             # True
print(parsikit.detect_bank_from_sheba(sheba))     # 'بانک ملی ایران'
```

---

## 4. Postal Codes & Utility Bills

### Postal Code (کد پستی)
Validates 10-digit codes against postal layout rules (no 0 or 2 in certain positions) and formats as 5-5:

```python
import parsikit

print(parsikit.is_valid_postal_code("1417466191"))  # True
print(parsikit.format_postal_code("1417466191"))    # '14174-66191'
```

### Utility Bills (شناسه قبض و پرداخت)
Checks electricity, water, gas, and telephone bills and calculates payable amounts:

```python
import parsikit

bill_id = "982765410123"
pay_id = "12500345"
# Verifies check digits and parses bill metadata
```
