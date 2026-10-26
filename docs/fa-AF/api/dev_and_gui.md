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
چاپ گزارش ساختاریافته و رنگه در خروجی ترمینال.

### `validate_batch(items: list, model_class, silent: bool = False) -> dict`
اعتبارسنجی همزمان دسته‌ای از اقلام خام بر اساس یکی از مودل‌های دامنه‌ی پارسی‌کیت و گزارش موارد معتبر و نامعتبر.

---

## بازآرایی و مدیریت ورودی گرافیکی (`parsikit.reshaper`, `parsikit.gui`)

### `reshape_for_graphics(text: str, reverse: bool = True) -> str`
بازآرایی حروف متصل و معکوس‌سازی ترتیب کلمات جهت رندر صحیح در موتورهای ۲بعدی فاقد HarfBuzz (مانند Pillow, Pygame, OpenCV).

### `reshape_paragraph_for_graphics(text: str, max_chars_per_line: int, reverse: bool = True) -> list[str]`
شکستن و بازآرایی پاراگراف‌های طولانی به سطرهای متناسب جهت رسم در کادر تصویر.

### `bind_persian_input(widget, input_type: str = "text") -> None`
اتصال مدیریت تایپ زنده به فیلدهای ورودی کتابخانه‌های گرافیکی (Tkinter و CustomTkinter).
