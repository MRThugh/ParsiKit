# Роҳнамо: Бек-эндҳои веб (FastAPI ва Django)

Роҳнамои пайвастшавӣ ва истифодаи ParsiKit дар фреймворкҳои муосири веби Python:

---

## 1. Истифода дар FastAPI

Аз сабаби дастгирии моделҳои ParsiKit аз нақшаҳои Pydantic v2, метавонед онҳоро мустақиман дар схемаҳо ё параметрҳои масирҳо истифода намоед:

```python
from fastapi import FastAPI
import parsikit
from pydantic import BaseModel

app = FastAPI(title="API-и харид ва хизматрасонӣ")

class CheckoutRequest(BaseModel):
    customer_name: str
    national_code: parsikit.NationalCode
    mobile: parsikit.MobileNumber
    sheba: parsikit.Sheba

@app.post("/api/checkout")
def checkout(payload: CheckoutRequest):
    # Дурустии додаҳо пешакӣ комилан санҷида шудааст
    return {
        "status": "success",
        "customer": parsikit.standardize_persian(payload.customer_name),
        "national_code_masked": payload.national_code.masked,
        "mobile": payload.mobile.national,
        "bank": payload.sheba.bank_name,
    }
```

---

## 2. Истифода дар Django (Моделҳо ва формаҳо)

Истифодаи функсияҳои санҷиши эътибор дар майдонҳои махсус ё методи `clean`:

```python
from django.core.exceptions import ValidationError
from django.db import models
import parsikit

class NationalCodeField(models.CharField):
    description = "Рамзи миллии 10-рақама"

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 10
        super().__init__(*args, **kwargs)

    def validate(self, value, model_instance):
        super().validate(value, model_instance)
        if not parsikit.is_valid_national_code(value):
            raise ValidationError(
                "Рамзи воридшуда нодуруст аст.",
                code="invalid_national_code"
            )
```

---

## 3. Мидлвейри ҳамоҳангсозии ҷустуҷӯ дар пойгоҳи додаҳо

Барои мутобиқати дақиқи сатрҳои ҷустуҷӯ бо сабтҳои пойгоҳи додаҳо:

```python
def normalize_search_query(user_query: str) -> str:
    clean = parsikit.standardize_persian(user_query, strip_diacritics_opt=True)
    return clean
```
