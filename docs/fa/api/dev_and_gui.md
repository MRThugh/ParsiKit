# مرجع ابزارهای توسعه و گرافیک (`parsikit.dev`, `parsikit.gui`, `parsikit.reshaper`)

ابزارهای ویژه برای عیب‌یابی متنی، هم‌ترازی بصری در جدول‌ها، لاگ‌گیری و نمایش صحیح متن فارسی در رابط‌های گرافیکی (GUI).

---

## ۱. قالب‌بندی بصری هم‌تراز (`pformat` و `persian_fstring`)

کاراکترهای صفر-عرض مانند نیم‌فاصله (`\u200C`) و اعراب‌ها طول کاراکتری دارند اما عرض نمایشی ندارند؛ توابع استاندارد پایتون در قالب‌بندی ستونی متون فارسی این تفاوت را لحاظ نکرده و جداول را کج می‌کنند.

### `pformat(template: str, *args, **kwargs) -> str`
متن را با در نظر گرفتن عرض واقعی بصری (Visual Width) کاراکترها مرتب کرده و فاصله‌گذاری‌ها را هم‌تراز می‌کند. پشتیبانی از پیشوند `:fa` برای تبدیل هم‌زمان ارقام و ویرگول‌های هزارگان.

```python
from parsikit.dev import pformat

line = pformat("{:15} | {:>10:fa}", "کتاب‌ها", 15000)
print(line)  # 'کتاب‌ها         |     ۱۵،۰۰۰'
```

### `persian_fstring(template: str, **kwargs) -> str`
مانند `pformat` برای عبارات الگویی با پشتیبانی از نام متغیرها.

---

## ۲. ابزارهای عیب‌یابی و آزمایش (`parsikit.dev`)

### `inspect_text(text: str) -> dict`
ساختار متن را کالبدشکافی کرده و وضعیت نیم‌فاصله‌ها، ارقام، اعراب و نویسه‌های عربی را گزارش می‌دهد:
```python
from parsikit.dev import inspect_text

report = inspect_text("نمونه ۱۲۳")
print(report)
# {'length': ..., 'has_arabic_chars': False, 'has_zwnj': False, 'has_persian_digits': True, ...}
```

### `debug_text(text: str) -> None`
گزارش رنگی خوانا و تشخیصی از ویژگی‌های متن را در ترمینال چاپ می‌کند.

### `validate_batch(items: list, model_class, silent: bool = False) -> dict`
مجموعه‌ای از داده‌ها را به صورت دسته‌ای ارزیابی کرده و تعداد موارد معتبر و نامعتبر را به همراه خطاها تفکیک می‌کند.

---

## ۳. بازآرایی گرافیکی و اتصال به رابط کاربر (`parsikit.reshaper`, `parsikit.gui`)

### `reshape_for_graphics(text: str, reverse: bool = True) -> str`
متن فارسی را برای موتورهای رندر فاقد موتور HarfBuzz (مانند Pygame، Pillow، OpenCV و ReportLab) شکل‌دهی و دوجهته‌سازی می‌کند.

### `reshape_paragraph_for_graphics(text: str, max_chars_per_line: int, reverse: bool = True) -> str`
پاراگراف چندخطی را شکسته و هر سطر را به صورت متصل و آینه‌ای آماده رسم می‌کند.

### `bind_persian_input(widget, input_type: str = "text") -> None`
یک ویجت ورودی متنی در فریم‌ورک‌های Tkinter یا CustomTkinter را مجهز به دستیار تایپ فارسی خودکار (تبدیل «ي» و «ك» و اصلاح اعداد) می‌نماید.
