# Tutorial: Persian Text Processing & Standardization

Handling Persian text in software requires handling distinct Unicode quirks: Arabic character substitution, Zero-Width Non-Joiner (ZWNJ) boundaries, diacritic marks, and mixed digit scripts.

---

## 1. Character Standardization

Users frequently enter Arabic letterforms from mismatched keyboard layouts:
- Arabic Yeh (`ي` / `\u064A`) instead of Persian Yeh (`ی` / `\u06CC`)
- Arabic Kaf (`ك` / `\u0643`) instead of Persian Keheh (`ک` / `\u06A9`)
- Arabic Teh Marbuta (`ة` / `\u0629`)

`standardize_persian` unifies these into canonical Persian characters:

```python
import parsikit

dirty = "اين يك متن پيچيده با كدملي است."
clean = parsikit.standardize_persian(dirty)
print(clean)
# 'این یک متن پیچیده با کدملي است.'
```

---

## 2. Zero-Width Non-Joiner (ZWNJ / نیم‌فاصله)

In Persian grammar, verbal prefixes (`می‌`, `نمی‌`) and grammatical suffixes (`‌ها`, `‌ترین`, `‌مند`) require a half-space (ZWNJ, `\u200C`) rather than a full ASCII space.

```python
import parsikit

raw = "کتاب ها می روند و بر می گردند"
clean = parsikit.standardize_persian(raw)
print(clean)
# 'کتاب‌ها می‌روند و برمی‌گردند'
```

---

## 3. Stripping Diacritics (اعراب‌زدایی)

Diacritics (َ ِ ُ ً ٍ ٌ ّ ْ) can interfere with database searching and full-text index lookups:

```python
import parsikit

vowelized = "سَلامٌ عَلَیکُم وَ رَحمَةُ الله"
clean = parsikit.strip_diacritics(vowelized)
print(clean)
# 'سلام علیکم و رحمة الله'
```

---

## 4. Converting Mistyped English Keyboards

When a user types on an English keyboard layout while intending to type Persian:

```python
import parsikit

mistyped = "sghl phgaj,k ],ji?"
persian = parsikit.correct_keyboard_layout(mistyped)
print(persian)
# 'سلام حالتون چطوره؟'
```

---

## 5. SEO URL Slug Generation (`slugify`)

ParsiKit includes an intelligent Persian transliteration dictionary to turn Persian article titles into readable Finglish slugs:

```python
import parsikit

title = "معرفی نسخه جدید پارسی کیت"
slug = parsikit.slugify(title)
print(slug)
# 'moarefi-neskheh-jadid-parsi-kit'
```
