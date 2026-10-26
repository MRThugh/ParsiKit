# رهنمود: سیستم‌های بک‌اند وب (FastAPI و Django)

رهنمود نحوه‌ی اتصال و استفاده از ParsiKit در فریم‌ورک‌های وب مدرن پایتون:

---

## ۱. استفاده در FastAPI

به دلیل پشتیبانی بومی مودل‌های دامنه از Pydantic v2، می‌توانید آن‌ها را مستقیماً به عنوان نوعیت فیلدها در اسکیماها یا پارامترهای روت‌ها استفاده نمایید:

```python
from fastapi import FastAPI
import parsikit
from pydantic import BaseModel

app = FastAPI(title="سامانه‌ی فروش و خدمات")

class CheckoutRequest(BaseModel):
    customer_name: str
    national_code: parsikit.NationalCode
    mobile: parsikit.MobileNumber
    sheba: parsikit.Sheba

@app.post("/api/checkout")
def checkout(payload: CheckoutRequest):
    # صحت داده‌ها قبلاً به گونه‌ی کامل تصدیق گردیده است
    return {
        "status": "success",
        "customer": parsikit.standardize_persian(payload.customer_name),
        "national_code_masked": payload.national_code.masked,
        "mobile": payload.mobile.national,
        "bank": payload.sheba.bank_name,
    }
```

---

## ۲. استفاده در Django (مودل‌ها و فورم‌ها)

استفاده از توابع اعتبارسنجی در فیلدهای اختصاصی یا متد `clean`:

```python
from django.core.exceptions import ValidationError
from django.db import models
import parsikit

class NationalCodeField(models.CharField):
    description = "شناسه ملی ۱۰ رقمی"

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 10
        super().__init__(*args, **kwargs)

    def validate(self, value, model_instance):
        super().validate(value, model_instance)
        if not parsikit.is_valid_national_code(value):
            raise ValidationError(
                "کود شناسه واردشده معتبر نمی‌باشد.",
                code="invalid_national_code"
            )
```

---

## ۳. میدل‌ویر معیارسازی جستجو در دیتابیس

جهت انطباق دقیق عبارات جستجو شده با رکوردهای پایگاه داده:

```python
def normalize_search_query(user_query: str) -> str:
    clean = parsikit.standardize_persian(user_query, strip_diacritics_opt=True)
    return clean
```
