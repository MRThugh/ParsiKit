# مرجع ماژول‌های عیب‌یابی و واسط گرافیکی (`parsikit.dev`, `parsikit.gui`)

---

## تراز دیداری و عیب‌یابی متن (`parsikit.dev`)

### `pformat(template: str, *args, **kwargs) -> str`
قالب‌بندی هوشمند متن که اثر کاراکترهای با پهنای صفر (نیم‌فاصله، اعراب) را خنثی ساخته و تراز ستون‌ها را بر اساس پهنای دیداری روی صفحه محاسبه می‌کند. از نشانه‌های `:fa` و `:p` برای تبدیل خودکار ارقام پشتیبانی می‌نماید.

### `persian_fstring(template: str, **kwargs) -> str`
ارزیابی رشته‌های قالب‌بندی‌شده با استخراج خودکار متغیرهای اسکوپ پیرامونی و اعمال تراز دیداری.

### `inspect_text(text: str) -> dict`
تحلیل موشگافانه‌ی متن و ارائه‌ی گزارش آماری از تعداد حروف، نیم‌فاصله‌ها، حروف عربی و وضعیت ارقام همراه با رهنمودهای پیشنهادی.

### `debug_text(text: str) -> None`
چاپ گزارش ساختاریافته و رنگه در خروجی ترمینال با رعایت استانداردهای `NO_COLOR`، `FORCE_COLOR`، ترمینال ویندوز (`WT_SESSION`) و ConEmu.

### `validate_batch(items: list, model_class, silent: bool = False) -> dict`
اعتبارسنجی همزمان دسته‌ای از اقلام خام بر اساس یکی از مودل‌های دامنه‌ی پارسی‌کیت و گزارش موارد معتبر و نامعتبر.

---

## بازآرایی و مدیریت ورودی گرافیکی (`parsikit.reshaper`, `parsikit.gui`)

### `reshape_for_graphics(text: str, reverse: bool = True) -> str`
بازآرایی حروف متصل و معکوس‌سازی ترتیب کلمات جهت رندر صحیح در موتورهای ۲بعدی فاقد HarfBuzz (مانند Pillow, Pygame, OpenCV).

### `reshape_paragraph_for_graphics(text: str, max_chars_per_line: int, reverse: bool = True) -> list[str]`
شکستن و بازآرایی پاراگراف‌های طولانی به سطرهای متناسب جهت رسم در کادر تصویر.

### `bind_persian_input(widget, input_type: str = "text", *, digit_style: str = "auto", smart_spacing: bool = False, snippets: dict[str, str] | None = None, enable_shortcuts: bool = True) -> None`
اتصال مدیریت تایپ زنده به فیلدهای ورودی کتابخانه‌های گرافیکی:
- **ابزارهای پشتیبانی‌شده**:
  - جعبه‌های ورودی Tkinter (`tk.Entry`, `tk.Text`)
  - ابزارهای CustomTkinter (`ctk.CTkEntry`)
  - فریم‌ورک Qt (`QLineEdit`, `QTextEdit`, `QPlainTextEdit` در PyQt5, PyQt6, PySide2, PySide6)
- **حفظ هوشمندانه‌ی موقعیت کرسر**:
  - جلوگیری از پرش کرسر به انتهای سطر هنگام تایپ یا ویرایش در میان متن.
- **پارامترها**:
  - `input_type`: نوع ورودی شامل `"text"`, `"national_code"`, `"mobile"`, `"card"`, یا `"sheba"`.
  - `digit_style`: سبک تبدیل ارقام (`"auto"`, `"persian"`, `"english"`, یا `"none"`).
  - `smart_spacing`: فعال‌سازی اصلاح خودکار نیم‌فاصله.
  - `snippets`: دیکشنری میانبرهای متنی.
  - `enable_shortcuts`: فعال‌سازی کلیدهای میانبر نظیر Shift+Space.

### `unbind_persian_input(widget) -> None`
قطع مصئون ارتباط کنترل‌کننده‌های تایپ از ویجت گرافیکی.
