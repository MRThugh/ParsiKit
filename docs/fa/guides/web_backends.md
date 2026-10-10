# راهنمای استفاده از پارسی‌کیت در وب‌سرویس‌ها (FastAPI و Django)

پارسی‌کیت به لطف قابلیت duck-typing و پشتیبانی بومی از Pydantic، بهترین گزینه برای تمیزکاری و اعتبارسنجی ورودی‌ها در APIهای پایتونی است.

---

## ۱. استفاده در FastAPI با Pydantic

مدل‌های پارسی‌کیت مستقیماً به عنوان نوع داده در فیلدهای Pydantic کار می‌کنند:

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import parsikit

app = FastAPI(title="سامانه پرداخت ایرانی")

class UserRegisterSchema(BaseModel):
    name: str
    national_code: parsikit.NationalCode
    mobile: parsikit.MobileNumber
    card: parsikit.BankCard

@app.post("/register")
def register_user(payload: UserRegisterSchema):
    # تمام فیلدها در لحظه ورود اعتبارسنجی شده‌اند
    return {
        "status": "success",
        "clean_national_code": payload.national_code.clean,
        "masked_card": payload.card.masked,
        "bank_name": payload.card.bank["name"] if payload.card.bank else None,
        "mobile_international": payload.mobile.to_international(),
        "operator": payload.mobile.operator,
    }
```

اگر کاربر کد ملی نامعتبر بفرستد، FastAPI خودکار خطای اعتبارسنجی HTTP 422 برمی‌گرداند.

---

## ۲. استفاده در جنگو (Django Forms & Serializers)

در فرم‌های جنگو می‌توانید در متدهای `clean_<field>` اعتبارسنجی را صدا بزنید:

```python
from django import forms
from django.core.exceptions import ValidationError
import parsikit

class IranianUserProfileForm(forms.Form):
    national_code = forms.CharField(max_length=10)
    mobile = forms.CharField(max_length=15)

    def clean_national_code(self):
        code = self.cleaned_data["national_code"]
        if not parsikit.is_valid_national_code(code):
            raise ValidationError("کد ملی وارد شده نامعتبر است.")
        return parsikit.NationalCode(code).clean

    def clean_mobile(self):
        phone = self.cleaned_data["mobile"]
        if not parsikit.is_valid_mobile(phone):
            raise ValidationError("شماره موبایل نامعتبر است.")
        return parsikit.normalize_mobile(phone, prefix="0")
```

---

## ۳. تمیزکاری دیتای متنی قبل از ذخیره در دیتابیس

قبل از ذخیره توضیحات، بیو یا نام کاربران، اجرای `clean_text` جستجوی دیتابیس را تضمین می‌کند:

```python
cleaned_title = parsikit.clean_text(user_input_title)
```
این کار تمام حروف عربی «ي» و «ك» را پاکسازی کرده و نیم‌فاصله‌های استاندارد تولید می‌کند.
