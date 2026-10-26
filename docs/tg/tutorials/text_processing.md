# Омӯзиш: Коркарди матн ва танзими нимафосилаҳо

Идораи дурусти матн дар нармафзорҳо ҳалли ихтилофи сафҳакалидҳо, нимафосилаҳо, эъроб ва рақамҳои омехтаро талаб мекунад.

---

## 1. Ҳамоҳангсозии ҳарфҳо

Корбарон аксар вақт бо сабаби сафҳакалид ҳарфҳои нодуруст ворид мекунанд:
- Ҳарфи «ي»-и арабӣ ба ҷои «ی»
- Ҳарфи «ك»-и арабӣ ба ҷои «ک»

Функсияи `standardize_persian` ин ҳарфҳоро ба шакли расмӣ медарорад:

```python
import parsikit

dirty = "اين يك متن پيچيده با كد است."
clean = parsikit.standardize_persian(dirty)
print(clean)
# 'این یک متن پیچیده با کد است.'
```

---

## 2. Танзими нимафосилаҳо (ZWNJ)

Пешвандҳо ва пасвандҳо ниёз ба нимафосила (`\u200C`) доранд:

```python
import parsikit

raw = "کتاب ها می روند و بر می گردند"
clean = parsikit.standardize_persian(raw)
print(clean)
# 'کتاب‌ها می‌روند و برمی‌گردند'
```

---

## 3. Ҳазфи эъроб ва аломатҳои ҳаракат

```python
import parsikit

vowelized = "سَلامٌ عَلَیکُم وَ رَحمَةُ الله"
clean = parsikit.strip_diacritics(vowelized)
print(clean)
# 'سلام علیکم و رحمة الله'
```

---

## 4. Ислоҳи матни бо сафҳакалиди англисӣ чопшуда

```python
import parsikit

mistyped = "sghl phgaj,k ],ji?"
persian = parsikit.correct_keyboard_layout(mistyped)
print(persian)
# 'سلام حالتون چطوره؟'
```

---

## 5. Тавлиди сатрҳои СЭО (`slugify`)

```python
import parsikit

title = "Муаррифии версияи нави ParsiKit"
slug = parsikit.slugify(title)
print(slug)
```
