# Омӯзиш: Тақвими шамсӣ ва вақти нисбӣ

Тақвими ҳиҷрии шамсӣ (ҷалолӣ) тақвими офтобӣ мебошад. ParsiKit алгоритмҳои дақиқи астрономиро бидуни вобастагиҳои иловагӣ таъмин менамояд.

---

## 1. Табдили санаи милодӣ ба шамсӣ

```python
import parsikit

# Табдили санаи милодӣ (сол, моҳ, рӯз)
jy, jm, jd = parsikit.gregorian_to_jalali(2026, 7, 6)
print(f"Санаи шамсӣ: {jy}/{jm:02d}/{jd:02d}")
# Натиҷа: Санаи шамсӣ: 1405/04/15

# Номи моҳ
month_name = parsikit.get_jalali_month_name(jm)
print(f"{jd} {month_name} {jy}")
# Натиҷа: 15 تیر 1405
```

---

## 2. Табдили санаи шамсӣ ба милодӣ

```python
import parsikit

gy, gm, gd = parsikit.jalali_to_gregorian(1405, 4, 15)
print(f"Санаи милодӣ: {gy}-{gm:02d}-{gd:02d}")
# Натиҷа: Санаи милодӣ: 2026-07-06
```

---

## 3. Муайян кардани соли кабиса

Дар тақвими шамсӣ, солҳои оддӣ 365 рӯз ва солҳои кабиса 366 рӯз мебошанд:

```python
import parsikit

print(parsikit.is_jalali_leap(1399))  # True
print(parsikit.is_jalali_leap(1400))  # False
print(parsikit.is_jalali_leap(1403))  # True
print(parsikit.is_jalali_leap(1404))  # False
```

---

## 4. Ифодаи вақти нисбӣ бо сухани табиӣ

Табдили сонияҳо ё объекти вақт ба ибораи фаҳмо:

```python
import datetime
import parsikit

# 5 дақиқа пеш
print(parsikit.humanize_relative_time(-300))
# Натиҷа: ۵ دقیقه پیش

# 3 соат пеш
print(parsikit.humanize_relative_time(-10800))
# Натиҷа: ۳ ساعت پیش

# Пас аз фардо
print(parsikit.humanize_relative_time(2 * 86400))
# Натиҷа: پس‌فردا
```
