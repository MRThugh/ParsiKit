# Омӯзиш: Санҷиши эътибори рамзҳо ва ҳуҷҷатҳои расмӣ

Муҳаррикҳои санҷиши эътибори ParsiKit барои муайян кардани дурустии сохтори ҳуҷҷатҳо:

---

## 1. Рамзи миллӣ (National Code)

Рамзи миллӣ шумораи 10-рақама мебошад, ки рақами даҳуми он чек-сами расмӣ дар асоси бақияи тақсим ба 11 бо вазнҳои аз 10 то 2 мебошад:

```python
import parsikit

# Санҷиши эътибор
print(parsikit.is_valid_national_code("0010123458"))  # True
print(parsikit.is_valid_national_code("1111111111"))  # False (рақамҳои такрорӣ)
print(parsikit.is_valid_national_code("0010123451"))  # False (чек-сами нодуруст)

# Қолаббандӣ
print(parsikit.format_national_code("0010123458"))    # '001-012345-8'

# Муайян кардани маҳалли судур
print(parsikit.detect_national_code_location("0010123458"))
# {'province': 'تهران', 'city': 'تهران مرکزی'}
```

---

## 2. Рақамҳои телефони мобилӣ

```python
import parsikit

phone = "+989123456789"
print(parsikit.is_valid_mobile(phone))           # True
print(parsikit.normalize_mobile(phone, "0"))     # '09123456789'
print(parsikit.detect_mobile_operator(phone))    # 'MCI'
```

---

## 3. Кортҳои бонкӣ ва рақами суратҳисоб (IBAN)

### Кортҳои 16-рақама
Санҷиши алгоритми Лун ва муайян кардани бонки содиркунанда:

```python
import parsikit

card = "6037991122334455"
print(parsikit.is_valid_card_number(card))       # True
print(parsikit.format_card_number(card))         # '6037-9911-2233-4455'
print(parsikit.detect_bank_from_card(card))      # 'بانک ملی ایران'
```

### Суратҳисоби бонкӣ (IBAN / Sheba)
Санҷиши 24 рақам тибқи ISO 7064 Mod 97-10:

```python
import parsikit

sheba = "IR120170000000123456789012"
print(parsikit.is_valid_sheba(sheba))             # True
print(parsikit.detect_bank_from_sheba(sheba))     # 'بانک ملی ایران'
```

---

## 4. Рамзи почта ва ҳисобномаҳо

```python
import parsikit

# Рамзи почтаи 10-рақама
print(parsikit.is_valid_postal_code("1417466191"))  # True
print(parsikit.format_postal_code("1417466191"))    # '14174-66191'

# Рамзи пардохт ва ҳисобнома
bill_id = "982765410123"
pay_id = "12500345"
```
