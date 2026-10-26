# رهنمود: اعتبارسنجی فورم‌ها و مصئونیت داده‌های حساس

مدیریت معلومات تشخیص هویت فردی (PII) همچون کودهای شناسایی، شماره‌های کارت بانکی و شماره‌های تلفون نیازمند رعایت الزامات امنیتی دقیق است تا از افشای آن‌ها در لاگ‌های سیستمی و پنل‌های مدیریتی جلوگیری به عمل آید.

---

## ۱. پاک‌کاری داده‌های ورودی قبل از ذخیره‌سازی

همواره ورودی‌های متنی کاربران را پیش از ذخیره در پایگاه داده معیارسازی کنید:

```python
import parsikit

def sanitize_user_input(raw_full_name: str, raw_address: str):
    return {
        "full_name": parsikit.clean_text(raw_full_name),
        "address": parsikit.beautify_persian_spacing(parsikit.clean_text(raw_address)),
    }
```

---

## ۲. پیشگیری از نشت اطلاعات حساس در لاگ‌ها

حین ثبت تراکنش‌ها یا رویدادها، هرگز ارقام خام کارت‌ها یا شناسه‌ها را لاگ نکنید. از خاصیت `.masked` یا توابع `mask_*` استفاده نمایید:

```python
import logging
import parsikit

logger = logging.getLogger("payment")

def process_payment(card_number_raw: str, national_code_raw: str):
    card = parsikit.BankCard(card_number_raw)
    nc = parsikit.NationalCode(national_code_raw)

    # ثبت مصئون با اطلاعات ماسک‌شده
    logger.info(
        "پردازش پرداخت کاربر (کود شناسایی: %s) با کارت: %s (%s)",
        nc.masked,
        card.masked,
        card.bank_name,
    )
```

---

## ۳. مدیریت مصئون استثنائات

در ParsiKit نسخه v3.3.1 تمامی پیام‌های خطای استثنائات به گونه‌ی پیش‌فرض پالایش شده‌اند تا دیتای خام در ردگیری خطاها (Stack Traces) ظاهر نشود:

```python
import parsikit

try:
    card = parsikit.BankCard("6037991122339999")
except parsikit.InvalidCardNumberError as exc:
    # پیام استثنا حاوی ارقام محرمانه کارت نیست
    logger.warning("خطا در پرداخت: %s", exc)
```
