# Омӯзиш: Рақамҳо ва ҳисобҳои молиявӣ дар Python

Ин дастур табдили рақамҳо, адад ба калимаҳо, қолаббандии маблағҳо ва ҳисоби фоизҳои қарзро намоиш медиҳад.

---

## 1. Табдили хатти рақамҳо

Табдили рақамҳои шарқӣ (`۰-۹`), арабӣ (`٠-٩`) ва англисӣ (`0-9`):

```python
import parsikit

# Англисӣ ба шарқӣ
print(parsikit.english_to_persian("ID-и корбар: 1042"))
# 'ID-и корбар: ۱۰۴۲'

# Шарқӣ/арабӣ ба англисӣ
print(parsikit.persian_to_english("Маблағ: ۲۵۰۰۰ ریال"))
# 'Маблағ: 25000 ریال'
```

---

## 2. Табдили ададҳо ба калимаҳои хаттӣ

Табдили зудамали ададҳои калон бо ёрии кэши дохилӣ:

```python
import parsikit

print(parsikit.number_to_words(0))
# 'صفر'

print(parsikit.number_to_words(1250000))
# 'یک میلیون و دویست و پنجاه هزار'

print(parsikit.number_to_words(-42))
# 'منفی چهل و دو'
```

---

## 3. Табдили асъор (Риёл ва Тумон)

```python
import parsikit

# Риёл ба тумон (тақсим ба 10)
print(parsikit.rial_to_toman(500000))  # 50000

# Тумон ба риёл (зарб ба 10)
print(parsikit.toman_to_rial(50000))   # 500000

# Қолаббандӣ бо ҷудокунандаи серақама
print(parsikit.format_currency(12500000, "toman", persian_digits=True))
# '۱۲،۵۰۰،۰۰۰ تومان'

# Навиштани маблағ бо калимаҳо
print(parsikit.format_currency_to_words(12500000, "toman"))
# 'دوازده میلیون و پانصد هزار تومان'
```

---

## 4. Ҳисоби андоз аз арзиши иловашуда (ААИ)

Ҳисоби андоз тибқи меъёри муқарраршуда (пешфарз: 10%):

```python
import parsikit

invoice = parsikit.add_tax_and_toll(10000000)
print(f"Маблағи асосӣ: {invoice['original_amount']:,}")
print(f"Андоз ({invoice['tax_rate']*100}%): {invoice['tax_amount']:,}")
print(f"Маблағи умумӣ: {invoice['total_amount']:,}")
```

---

## 5. Ҳисоби пардохтҳои моҳонаи қарз (Installments)

```python
import parsikit

# Қарзи 100 миллион бо фоизи солонаи 23% ба муҳлати 24 моҳ
loan = parsikit.calculate_installments(100_000_000, 23.0, 24)

print("Пардохти моҳона:", loan['monthly_installment'])
print("Бозпардохти умумӣ:", loan['total_payment'])
print("Фоизи умумӣ:", loan['total_interest'])
```
