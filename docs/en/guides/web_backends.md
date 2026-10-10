# Guide: Web Backends (FastAPI & Django Integration)

This guide shows how to integrate ParsiKit into production web backends.

---

## 1. FastAPI Integration

Because ParsiKit domain models natively support Pydantic v2 core schemas, you can declare them directly as request body or query parameter types.

```python
from fastapi import FastAPI, HTTPException
import parsikit

app = FastAPI(title="Iranian E-Commerce API")

from pydantic import BaseModel

class CheckoutRequest(BaseModel):
    customer_name: str
    national_code: parsikit.NationalCode
    mobile: parsikit.MobileNumber
    sheba: parsikit.Sheba

@app.post("/api/checkout")
def checkout(payload: CheckoutRequest):
    # Data is already guaranteed valid when execution reaches here!
    return {
        "status": "success",
        "customer": parsikit.standardize_persian(payload.customer_name),
        "national_code_masked": payload.national_code.masked,
        "mobile": payload.mobile.national,
        "bank": payload.sheba.bank_name,
    }
```

---

## 2. Django Model & Form Validation

In Django, use ParsiKit validators inside clean methods or custom model fields:

```python
from django.core.exceptions import ValidationError
from django.db import models
import parsikit

class IranianNationalCodeField(models.CharField):
    description = "Iranian 10-digit National Code"

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 10
        super().__init__(*args, **kwargs)

    def validate(self, value, model_instance):
        super().validate(value, model_instance)
        if not parsikit.is_valid_national_code(value):
            raise ValidationError(
                f"کد ملی وارد شده معتبر نمی‌باشد.",
                code="invalid_national_code"
            )
```

---

## 3. Database Query Normalization Middleware

To ensure search queries match records in PostgreSQL or MySQL regardless of whether the user typed Arabic Yeh (`ي`) or Persian Yeh (`ی`):

```python
def normalize_search_query(user_query: str) -> str:
    clean = parsikit.standardize_persian(user_query, strip_diacritics_opt=True)
    return clean
```
