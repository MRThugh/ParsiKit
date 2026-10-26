# Роҳнамо: Санҷиши формаҳо ва амнияти додаҳои ҳассос

Мудирияти маълумоти мушаххаси шахсӣ (PII) ба монанди рамзҳои шиносоӣ, рақамҳои корти бонкӣ ва рақамҳои телефон риояи меъёрҳои қатъии амниятиро талаб мекунад, то аз фош шудани онҳо дар сабти рӯйдодҳо (логҳо) ва панелҳои идоракунӣ ҷилавгирӣ шавад.

---

## 1. Поксозии додаҳои воридотӣ пеш аз сабт

Ҳамеша матнҳои воридкардаи корбаронро қабл аз ворид кардан ба пойгоҳи додаҳо стандартсозӣ намоед:

```python
import parsikit

def sanitize_user_input(raw_full_name: str, raw_address: str):
    return {
        "full_name": parsikit.clean_text(raw_full_name),
        "address": parsikit.beautify_persian_spacing(parsikit.clean_text(raw_address)),
    }
```

---

## 2. Пешгирӣ аз ихроҷи иттилооти ҳассос дар логҳо

Ҳангоми сабти амалиёт ва рӯйдодҳо, ҳаргиз рақамҳои хоми кортҳо ё рамзҳои шахсиро нанависед. Аз хосияти `.masked` ё функсияҳои `mask_*` истифода намоед:

```python
import logging
import parsikit

logger = logging.getLogger("payment")

def process_payment(card_number_raw: str, national_code_raw: str):
    card = parsikit.BankCard(card_number_raw)
    nc = parsikit.NationalCode(national_code_raw)

    # Сабти амн бо иттилооти ниқоббаста
    logger.info(
        "Пардохти корбар (Рамз: %s) бо корти: %s (%s)",
        nc.masked,
        card.masked,
        card.bank_name,
    )
```

---

## 3. Мудирияти бехатари истисноҳо

Дар ParsiKit версияи v3.3.1 ҳамаи паёмҳои хатогии истисноҳо ба таври пешфарз тоза карда шудаанд, то маълумоти махфӣ дар пайгирии хатогиҳо (Stack Traces) намоён нашавад:

```python
import parsikit

try:
    card = parsikit.BankCard("6037991122339999")
except parsikit.InvalidCardNumberError as exc:
    # Паёми истисно рақамҳои махфии кортро дар бар намегирад
    logger.warning("Хатогӣ дар пардохт: %s", exc)
```
