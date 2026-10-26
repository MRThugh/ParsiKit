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
گزارش رنگی خوانا و تشخیصی از ویژگی‌های متن را در ترمینال چاپ می‌کند. خروجی رنگی از استانداردهای مدرن `NO_COLOR`، `FORCE_COLOR`، ترمینال ویندوز (`WT_SESSION`) و ConEmu تبعیت می‌کند.

### `validate_batch(items: list, model_class, silent: bool = False) -> dict`
مجموعه‌ای از داده‌ها را به صورت دسته‌ای ارزیابی کرده و تعداد موارد معتبر و نامعتبر را به همراه خطاها تفکیک می‌کند.

---

## ۳. بازآرایی گرافیکی و اتصال به رابط کاربر (`parsikit.reshaper`, `parsikit.gui`)

### `reshape_for_graphics(text: str, reverse: bool = True) -> str`
متن فارسی را برای موتورهای رندر فاقد موتور HarfBuzz (مانند Pygame، Pillow، OpenCV و ReportLab) شکل‌دهی و دوجهته‌سازی می‌کند.

### `reshape_paragraph_for_graphics(text: str, max_chars_per_line: int, reverse: bool = True) -> str`
پاراگراف چندخطی را شکسته و هر سطر را به صورت متصل و آینه‌ای آماده رسم می‌کند.

### `bind_persian_input(widget, input_type: str = "text", *, digit_style: str = "auto", smart_spacing: bool = False, snippets: dict[str, str] | None = None, enable_shortcuts: bool = True) -> None`
ویجت‌های ورودی متنی را در فریم‌ورک‌های گرافیکی به دستیار تایپ فارسی زنده مجهز می‌سازد:
- **فریم‌ورک‌های پشتیبانی‌شده**:
  - فریم‌ورک Tkinter: ویجت‌های `tk.Entry` و `tk.Text`
  - فریم‌ورک CustomTkinter: ویجت `ctk.CTkEntry`
  - فریم‌ورک Qt: ویجت‌های `QLineEdit`، `QTextEdit` و `QPlainTextEdit` در نسخه‌های PyQt5، PyQt6، PySide2 و PySide6
- **حفظ هوشمند مکان‌نما (Cursor Tracking)**:
  - با رهگیری موقعیت نسبی محتوا از پرش ناگهانی نشانگر به انتهای متن هنگام درج، حذف یا ویرایش در میانه کلمات جلوگیری می‌کند.
- **پارامترها**:
  - `input_type`: نوع ورودی شامل `"text"`، `"national_code"`، `"mobile"`، `"card"`، یا `"sheba"`.
  - `digit_style`: شیوه تبدیل ارقام (`"auto"`، `"persian"`، `"english"`، یا `"none"`).
  - `smart_spacing`: فعال‌سازی اصلاح خودکار نیم‌فاصله‌ها حین تایپ (`می‌` و `‌ها`).
  - `snippets`: دیکشنری جایگزینی میانبرهای متنی پرکاربرد (مثلاً `{"ق.ظ": "قبل از ظهر"}`).
  - `enable_shortcuts`: فعال‌سازی کلیدهای ترکیبی دستکتاپ مانند `Shift+Space` برای نیم‌فاصله در Tkinter.

### `unbind_persian_input(widget) -> None`
اتصال رویدادها، شنونده‌ها و سیگنال‌های کمکی تایپ فارسی را بدون ایجاد اختلال در ویجت قطع می‌نماید.
