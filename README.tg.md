<div align="center">

# 🌟 Китобхонаи ParsiKit 🌟
<p align="center">
  <img 
    src="https://raw.githubusercontent.com/MRThugh/MRThugh/main/badge.svg"
    width="50%" 
    alt="Нишони ParsiKit"
  />
</p>

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Author](https://img.shields.io/badge/author-Ali%20Kamrani-purple.svg)](https://github.com/MRThugh)
[![Version](https://img.shields.io/badge/version-3.3.1-blue.svg)](https://github.com/MRThugh/ParsiKit)
[![Official Website](https://img.shields.io/badge/сомона-parsikit-teal.svg)](https://mrthugh.github.io/parsikit-website/)

---

### 🌐 Нашрҳои забонӣ / Language Editions / Интихоби забон

| Забон | Рамзи маҳал (Locale) | Файли README | Маркази ҳуҷҷатгузорӣ | Самти навишт |
|---|---|---|---|---|
| **Тоҷикӣ (Тоҷикистон)** | `tg` | **[Дастури тоҷикӣ](README.tg.md)** | [Ҳуҷҷатгузории тоҷикӣ](docs/tg/index.md) | Чап-ба-рост (LTR) |
| **English** | `en` | **[English README](README.md)** | [English Docs](docs/en/index.md) | Чап-ба-рост (LTR) |
| **فارسی (ایران)** | `fa` | **[راهنمای فارسی](README.fa.md)** | [مستندات فارسی](docs/fa/index.md) | Рост-ба-чап (RTL) |
| **دری (افغانستان)** | `fa-AF` | **[رهنمود دری](README.fa-AF.md)** | [مستندات دری](docs/fa-AF/index.md) | Рост-ба-чап (RTL) |

---

**Зерсохтори мукаммал, баландсуръат ва холиси забони барномасозии Python барои коркарди матн, санҷиши эътибори додаҳо, ҳисобҳои молиявӣ, тақвими шамсии ҳиҷрӣ, бозсозии хатти графикӣ, ташхиси таҳиягарон ва ҳифзи амнияти маълумоти ҳассос.**

</div>

---

## 🔗 Пайвандҳои расмии лоиҳа

- **Сомонаи расмии ҳуҷҷатгузорӣ**: [https://mrthugh.github.io/parsikit-website/](https://mrthugh.github.io/parsikit-website/)
- **Манбаи рамзи китобхона дар GitHub**: [https://github.com/MRThugh/ParsiKit](https://github.com/MRThugh/ParsiKit)
- **Манбаи рамзи сомона**: [https://github.com/MRThugh/parsikit-website](https://github.com/MRThugh/parsikit-website)
- **Қайди хатогиҳо ва дархостҳо**: [https://github.com/MRThugh/ParsiKit/issues](https://github.com/MRThugh/ParsiKit/issues)
- **Таърихи тағйирот ва нашрҳо**: [CHANGELOG.md](CHANGELOG.md)
- **Меъмории система ва сохтори дохилӣ**: [docs/development/architecture.md](docs/development/architecture.md)
- **Роҳнамои саҳмгузорӣ ва ҳамкорӣ**: [docs/development/contributing.md](docs/development/contributing.md)

---

## 📖 Муаррифии ParsiKit

Китобхонаи **ParsiKit** (дар барномаҳо ба сурати `parsikit` ворид карда мешавад) як абзори мукаммал ва бидуни вобастагиҳои беруна (Zero-Dependency) мебошад, ки барои ҳалли тамоми мушкилоти кор бо додаҳо ва матнҳо дар забони барномасозии Python сохта шудааст.

Дар версияи **v3.3.1**, ParsiKit ба як **зерсохтори ҳамаҷонибаи барномасозӣ** табдил ёфтааст. Дар канори меъмории объекти нигаронидашуда (OOP) ва интерфейси муттаҳид, абзорҳои пешрафтаи ташхиси хатогиҳои матнӣ, қолаббандии мутобиқ ба паҳнои воқеии визуалӣ, абзорҳои амниятӣ (ниқоббандии иттилооти маҳрамона) ва шинохти худкори навъи додаҳо дастрас мебошанд.

---

## 🚀 Сутунҳои асосии меъморӣ дар версияи v3.3.1

### 1. Танзимоти саросарӣ ва нигаҳдории муваққатӣ (Кэш / Cache) бо амнияти бисёрриштагӣ (`parsikit.config` ва `parsikit.cache`)
* **Кэши зудамал ва бехатар**: Амалиёти вазнин ва такроршаванда (монанди табдили рақамҳои бузург ба калимаҳо ё ҳисобҳои тақвимӣ) бо механизми дохилии амни LRU (`ThreadSafeLRUCache`) суръат бахшида мешаванд.
* **Танзимоти саросарии содда**: Меъёри андоз аз арзиши иловашуда, воҳиди пулии пешфарз ё фаъолу хомӯш кардани кэшро дар саросари лоиҳа муайян намоед.

### 2. Истисноҳо ва хатогиҳои сохторёфта (`parsikit.exceptions`)
Дигар ниёз ба идоракунии хатогиҳои умумии `ValueError` ё `TypeError` нест. ParsiKit дарахти дақиқи истисноҳоро пешниҳод мекунад, ки барои меъмории тоза (Clean Architecture) комилан мувофиқ аст.

### 3. Моделҳои домейнӣ ва объекти нигаронидашуда (`parsikit.models`)
Сатрҳои хоми воридотиро ба моделҳои сохторёфта ба мисли `NationalCode`, `MobileNumber`, `BankCard`, `Sheba` ё `VehiclePlate` табдил диҳед. Ин моделҳо ҳангоми сохта шудан эътибори додаҳоро месанҷанд ва хусусиятҳои иловагиро фароҳам меоранд.

### 4. Ташхиси матн ва ҳамоҳангсозии визуалӣ (`parsikit.dev`)
* **Ҳамоҳангсозии паҳнои визуалӣ (`pformat` ва `persian_fstring`)**: Аломатҳои бепаҳно (монанди нимафосила ё эъроб) дар Python ҷойгоҳи рамзиро ишғол мекунанд, аммо дар экран паҳно надоранд. Ин боиси каҷ шудани сутунҳои ҷадвалҳо мегардад. ParsiKit паҳнои воқеиро ҳисоб карда, сутунҳоро комилан баробар месозад.
* **Ташхиси худкори нуқсонҳои матн**: Матнҳоро барои дарёфти ҳарфҳои номатлуби арабӣ, фосилаҳои зиёдатӣ ва нимафосилаҳои фаромӯшшуда санҷида, роҳнамоии ислоҳӣ гиред.

### 5. Поксозии ҳамаҷониба, сохтани слаг ва амнияти додаҳо (`parsikit.text`, `parsikit.validators`)
* **Сохтани слаги СЭО (`slugify`)**: Табдили унвонҳои матнӣ ба сатрҳои лотинии мувофиқ барои нишони вебсаҳифаҳо.
* **Поксозии саросарӣ (`clean_text` ва `normalize_whitespace`)**: Тоза кардани рамзҳои ноаёни Юникод, танзими нимафосилаҳо ва ҳазфи сатрҳои холии изофӣ.
* **Шинохти худкори навъи маълумот (`detect`)**: Муайян кардани худкори почтаи электронӣ (email), суроғаи веб (URL), рақами телефон, корти бонкӣ ва суратҳисобҳо.
* **Ниқоббандии маълумоти ҳассос (`mask_*`)**: Махфӣ сохтани қисмҳои мобайнии рақамҳои телефон, кортҳои бонкӣ ва рамзҳои миллӣ барои сабти бехатар дар логҳо (масалан `0912***6789`).

---

## ⚙️ Насб ва танзим

```bash
pip install parsikit
```

Барои навсозӣ ба версияи охирин:
```bash
pip install --upgrade parsikit
```

**Талаботи системавӣ: Python 3.10 ва болотар** (дар Python 3.10, 3.11, 3.12 ва 3.13 санҷида шудааст).

Барои дигар шеваҳои насб (Poetry, uv, venv ва рамзи ибтидоӣ), ба [Роҳнамои насб](docs/tg/installation.md) муроҷиат кунед.

---

## 🛠️ Идоракунии танзимот ва истисноҳо

### 1. Танзимоти саросарии рафтори китобхона
```python
import parsikit

# Танзими саросарии меъёри андоз (пешфарз: 0.10)
parsikit.config.default_tax_rate = 0.09

# Муайян кардани воҳиди пулии пешфарз (пешфарз: toman)
parsikit.config.default_currency = "rial"

# Фаъол кардани кэши коркард барои суръати бештар
parsikit.config.enable_cache = True
```

### 2. Сохтори истисноҳои махсус
Ҳама хатогиҳои санҷиши эътибор аз синфи `ValidationError` мерос мегиранд:
```python
import parsikit

try:
    card = parsikit.BankCard("invalid-card-number")
except parsikit.InvalidCardNumberError as e:
    print(f"Рақами корт нодуруст аст: {e}")
except parsikit.ValidationError as e:
    print(f"Хатогии умумии санҷиши эътибор: {e}")
```

---

## 🦄 Ҳамоҳангӣ бо Pydantic v2 ва FastAPI

Шумо метавонед синфҳои ParsiKit-ро мустақиман дар нақшаҳои Pydantic ва усулҳои FastAPI истифода баред:

```python
from fastapi import FastAPI
from pydantic import BaseModel
import parsikit

app = FastAPI()

class UserRegisterSchema(BaseModel):
    fullname: parsikit.PersianText
    national_id: parsikit.NationalCode
    phone: parsikit.MobileNumber
    card: parsikit.BankCard

@app.post("/register")
def register_user(user: UserRegisterSchema):
    # Ҳамаи додаҳо пешакӣ санҷида ва мутобиқ карда шудаанд!
    print(user.fullname.standardize()) # Ҳамоҳангсозии ҳарфҳо ва нимафосилаҳо
    print(user.national_id.location)   # Мавқеи ҷуғрофӣ
    print(user.phone.to_international()) # Рақами байналмилалӣ: "+989123456789"
    
    return {
        "status": "success",
        "data": {
            "national_id": user.national_id.to_dict(),
            "card_bank": user.card.bank
        }
    }
```

---

## 🚀 Намунаҳои рамз ва дастури имкониятҳо

### 1. Абзорҳои ташхиси таҳиягарон (`parsikit.dev`)

#### Ташхиси мукаммали матн
```python
import parsikit

analysis = parsikit.inspect_text("ي كافيه ك کتاب ها ميباشد ۱۲۳")
print(analysis["has_arabic_chars"]) # Натиҷа: True
print(analysis["has_zwnj_issues"])  # Натиҷа: True
print(analysis["suggestions"])

# Чопи ҳисоботи зебо дар терминали фармонҳо
parsikit.debug_text("ي كافيه ك کتاب ها ميباشد")
```

#### Намоиши хонои матн дар логҳо ва сохторҳои маълумот
```python
import parsikit

data = {"корбар": ["Амир", "Рустам"], "вазъият": True}

# Намоиши тоза бидуни рамзҳои нохонои Юникод:
print(parsikit.persian_repr(data))
# Натиҷа: {'корбар': ['Амир', 'Рустам'], 'вазъият': True}

# Чопи ранга ва ҷадвалбандишуда
parsikit.pretty_print(data, title="Маълумоти корбарон")
```

#### Санҷиши эътибори дастаҷамъӣ (Batch Validation)
```python
import parsikit

items = ["7730123452", "1111111111", "0010123451", "bad-code"]
report = parsikit.validate_batch(items, parsikit.NationalCode, silent=False)
```

---

### 2. Қолаббандӣ ва ҳамоҳангсозии визуалӣ (`pformat` ва `persian_fstring`)

#### Баробар кардани сутунҳо бо дарназардошти нимафосила
```python
import parsikit

# Калимаи "کتاب‌‌ها" дорои нимафосила мебошад
aligned = parsikit.pformat("{:<10} | тӯлонӣ", "کتاب‌‌ها")
print(aligned) # "کتاب‌‌ها   | тӯлонӣ"
```

#### Табдили рақамҳо тавассути пасванди қолаб
```python
import parsikit

print(parsikit.pformat("Арзиш: {:>10,fa} риёл", 1500000))
# Натиҷа: "Арзиш:  ۱،۵۰۰،۰۰۰ риёл"
```

---

### 3. Сохтани слаг ва поксозии матн

#### Сохтани сатрҳои СЭО (SEO Slugs)
```python
import parsikit

print(parsikit.slugify("Омӯзиши барномасозӣ бо забони содда"))
# Натиҷа: "amoozesh-barnamasazi-bo-zaboni-sodda"

print(parsikit.slugify("Салом ҷаҳон 💕"))
# Натиҷа: "salam-jahon"
```

#### Поксозии ҳамаҷонибаи матн (`clean_text`)
```python
import parsikit

dirty_text = "ي كافيه ك   کتاب  ها  ميباشد  ۱۱۲۳\n\n\n\nнав  "
print(parsikit.clean_text(dirty_text))
```

---

### 4. Санҷиши эътибор ва махфисозии маълумоти ҳассос

#### Муайянкунии худкори навъи маълумот (`detect`)
```python
import parsikit

print(parsikit.detect("09123456789")) # "mobile_number"
print(parsikit.detect("7730123452"))  # "national_code"
print(parsikit.detect("ali@example.com")) # "email"
print(parsikit.detect("192.168.1.1")) # "ip"
print(parsikit.detect("https://google.com")) # "url"
```

#### Ниқоббандии иттилооти маҳрамона
```python
import parsikit

# Ниқоббандии рақами телефон
print(parsikit.mask_mobile("09123456789"))
# Натиҷа: "0912***6789"

# Ниқоббандии корти бонкӣ
print(parsikit.mask_card("6037991122334455", mask_char="X"))
# Натиҷа: "6037-99XX-XXXX-4455"

# Ниқоббандии рамзи миллӣ
print(parsikit.mask_national_code("7730123452"))
# Натиҷа: "773-****45-2"

# Ниқоббандии суроғаи почтаи электронӣ
print(parsikit.mask_email("kamrani.exe@gmail.com"))
# Натиҷа: "ka******e@gmail.com"
```

---

### 5. Тақвими шамсӣ ва вақти нисбӣ

#### Табдили санаи милодӣ ба шамсӣ
```python
import parsikit
import datetime

# Табдили милодӣ ба шамсӣ бо суръати баланд ба воситаи кэш
jy, jm, jd = parsikit.gregorian_to_jalali(2026, 7, 5)
print(parsikit.format_jalali(jy, jm, jd, "YYYY-MM-DD"))
# Натиҷа: "1405-04-14"

# Санҷиши соли кабиса
print(parsikit.is_jalali_leap(1403)) # True

# Ифодаи вақти нисбӣ бо сухани табиӣ
posted_at = datetime.datetime.now() - datetime.timedelta(hours=3)
print(parsikit.humanize_relative_time(posted_at))
# Натиҷа: "۳ ساعت پیش"
```

#### Бозсозии хатти пайваста барои муҳаррикҳои графикӣ (Reshaper)
```python
import parsikit

shaped = parsikit.reshape_for_graphics("عَلِیّ", reverse=False)
print(shaped) # "ﻋَﻠِﻲّ"
```

---

## 🧪 Гузаронидани санҷишҳо (Тестҳо)

Маҷмӯаи мукаммали санҷишҳои сифат дар решаи лоиҳа ҷойгир аст:

```bash
python -m unittest test.py
# ё
pytest -v tests
```

---

## 👨‍💻 Муаллиф ва таҳиягар

**Алӣ Комронӣ (Ali Kamrani)**

- GitHub: [@MRThugh](https://github.com/MRThugh)
- Email: kamrani.exe@gmail.com
- Сомонаи расмии ҳуҷҷатгузорӣ: [https://mrthugh.github.io/parsikit-website/](https://mrthugh.github.io/parsikit-website/)

---

## 📄 Иҷозатнома (License)

Лоиҳа таҳти иҷозатномаи озоди **MIT** нашр шудааст. Истифода, тағйир ва паҳнкунии он дар тамоми лоиҳаҳои тиҷоратӣ ва озод комилан ройгон аст.

---

**ParsiKit** — Соддасозӣ ва баланд бардоштани сифати коркарди додаҳо дар барномасозӣ. 🚀
