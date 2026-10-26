# رهنمود نصب و عیارسازی ParsiKit

کتابخانه‌ی ParsiKit به پایتون نسخه‌ی **3.10** یا بالاتر نیاز دارد و کاملاً مستقل و فاقد هرگونه وابستگی بیرونی (Zero External Dependencies) است.

---

## ۱. نصب از طریق مخزن رسمی پایتون (PyPI)

ساده‌ترین شیوه برای نصب کتابخانه استفاده از ابزار `pip` است:

```bash
pip install parsikit
```

جهت ارتقا به تازه‌ترین نسخه‌ی باثبات:
```bash
pip install --upgrade parsikit
```

---

## ۲. نصب در محیط‌های مجازی (Virtual Environments)

### با استفاده از ماژول رسمی `venv`
```bash
python3 -m venv .venv
source .venv/bin/activate  # در سیستم‌عامل ویندوز: .venv\Scripts\activate
pip install parsikit
```

### با استفاده از Poetry
```bash
poetry add parsikit
```

### با استفاده از ابزار پُرشتاب uv
```bash
uv pip install parsikit
```

---

## ۳. نصب مستقیم از روی سورس گیت‌هاب

جهت توسعه و مشارکت یا استفاده از آخرین تغییرات شاخه‌ی اصلی:

```bash
git clone https://github.com/MRThugh/ParsiKit.git
cd ParsiKit
pip install -e .
```

---

## ۴. بررسی صحت نصب

برای اطمینان از نصب کامل و خوانش نگارش کتابخانه، دستور زیر را در ترمینال اجرا کنید:

```bash
python3 -c "import parsikit; print('ParsiKit version:', parsikit.__version__)"
```

خروجی باید نگارش `3.3.1` را نمایش دهد.
