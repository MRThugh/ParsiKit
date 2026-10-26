# Оғози фаврӣ бо ParsiKit (Quickstart)

Дар камтар аз 5 дақиқа бо бахшҳои асосии китобхонаи ParsiKit ошно шавед ва аввалин рамзҳоро иҷро намоед.

---

## 1. Ҳамоҳангсозӣ ва ислоҳи матн

```python
import parsikit

# Ислоҳи ҳарфҳои нодуруст ва танзими фосилаҳо
raw_text = "ي كافيه كتاب ها رو برداري و بري"
clean_text = parsikit.standardize_persian(raw_text)

print(clean_text)
# Натиҷа: ی کافیه کتاب‌ها رو برداری و بری
```

---

## 2. Санҷиши эътибори рамзи миллӣ

```python
import parsikit

code = "0010123458"
nc = parsikit.NationalCode(code)

print(nc.is_valid)   # True (мувофиқи алгоритми чек-сам)
print(nc.formatted)  # '001-012345-8'
print(nc.masked)     # '001-****45-8' (барои сабти бехатар дар логҳо)
print(nc.location)   # {'province': 'تهران', 'city': 'تهران مرکزی'}
```

---

## 3. Рақамҳо ва амалиёти молиявӣ

```python
import parsikit

amount = 1500000

# Қолаббандӣ бо ҷудокунандаи ҳазорҳо
formatted = parsikit.format_currency(amount, "toman", persian_digits=True)
print(formatted)
# Натиҷа: ۱،۵۰۰،۰۰۰ تومان

# Табдил ба калимаҳои хаттӣ
words = parsikit.number_to_words(amount)
print(f"{words} تومان")
# Натиҷа: یک میلیون و پانصد هزار تومان
```

---

## 4. Тақвими шамсӣ ва вақти нисбӣ

```python
import parsikit

# Табдили санаи милодӣ ба шамсӣ
jy, jm, jd = parsikit.gregorian_to_jalali(2026, 7, 6)
month_name = parsikit.get_jalali_month_name(jm)
print(f"{jd} {month_name} {jy}")
# Натиҷа: 15 تیر 1405

# Ифодаи вақти нисбӣ бо сухани табиӣ
print(parsikit.humanize_relative_time(-300))
# Натиҷа: ۵ دقیقه پیش
```

---

## 5. Рақамҳои телефон ва кортҳои бонкӣ

```python
import parsikit

# Рақами телефони мобилӣ
mobile = parsikit.MobileNumber("09123456789")
print(mobile.international)  # '+989123456789'
print(mobile.operator)       # 'MCI'
print(mobile.masked)         # '0912***6789'

# Корти бонкӣ
card = parsikit.BankCard("6037991122334455")
print(card.bank_name)        # 'بانک ملی ایران'
print(card.formatted)        # '6037-9911-2233-4455'
print(card.masked)           # '6037-99**-****-4455'
```
