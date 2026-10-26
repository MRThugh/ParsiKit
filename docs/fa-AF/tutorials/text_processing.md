# آموزش: پروسس متن و تنظیم نیم‌فاصله‌ها

مدیریت متن در نرم‌افزارها نیازمند حل تفاوت‌های کیبورد، نیم‌فاصله‌ها، اعراب و ارقام ترکیبی است.

---

## ۱. معیارسازی کاراکترها

کاربران معمولاً به دلیل تنظیمات کیبورد حروف عربی تایپ می‌کنند:
- «ي» عربی به جای «ی»
- «ك» عربی به جای «ک»
- «ة» تای مربوطه

تابع `standardize_persian` این حروف را معیارسازی می‌کند:

```python
import parsikit

dirty = "اين يك متن پيچيده با كد است."
clean = parsikit.standardize_persian(dirty)
print(clean)
# 'این یک متن پیچیده با کد است.'
```

---

## ۲. تنظیم نیم‌فاصله‌ها (ZWNJ)

پیشوندهای فعلی (`می‌`، `نمی‌`) و پسوندها (`‌ها`، `‌ترین`، `‌مند`) نیازمند نیم‌فاصله (`\u200C`) هستند:

```python
import parsikit

raw = "کتاب ها می روند و بر می گردند"
clean = parsikit.standardize_persian(raw)
print(clean)
# 'کتاب‌ها می‌روند و برمی‌گردند'
```

---

## ۳. حذف اعراب و حرکات

```python
import parsikit

vowelized = "سَلامٌ عَلَیکُم وَ رَحمَةُ الله"
clean = parsikit.strip_diacritics(vowelized)
print(clean)
# 'سلام علیکم و رحمة الله'
```

---

## ۴. اصلاح متن تایپ‌شده با کیبورد انگلیسی

```python
import parsikit

mistyped = "sghl phgaj,k ],ji?"
persian = parsikit.correct_keyboard_layout(mistyped)
print(persian)
# 'سلام حالتون چطوره؟'
```

---

## ۵. تولید اسلاگ سئو (`slugify`)

```python
import parsikit

title = "معرفی نسخه جدید پارسی کیت"
slug = parsikit.slugify(title)
print(slug)
# 'moarefi-neskheh-jadid-parsi-kit'
```
