# مرجع ماژول پردازش متن (`parsikit.text`)

مجموعه ابزارهای معیارسازی متون، تنظیم نیم‌فاصله‌ها، پاک‌کاری داده‌ها، تولید اسلاگ سئو و پنهان‌سازی معلومات حساس.

---

## معیارسازی و پالایش متن

### `standardize_persian(text: str, *, strip_diacritics_opt: bool = False, preserve_arabic: bool = False) -> str`
متن‌های ورودی را با رعایت دستور خط معیاری یکدست می‌سازد:
- تبدیل «ي» و «ك» عربی به معادل‌های معیاری («ی» و «ک»).
- حفظ کاراکترهای مختص کردی (مانند `ە`) و حفظ متون عربی در صورت فعال بودن `preserve_arabic=True`.
- تنظیم خودکار نیم‌فاصله‌ها (ZWNJ) برای پیشوندها (`می‌`، `نمی‌`) و پسوندها (`‌ها`، `‌ترین`).
- پاک‌سازی نیم‌فاصله‌های سرگردان، چسبیده به علائم نگارشی یا تکراری.
- حذف فضاهای خالی زاید بدون دستکاری شکست خطوط پاراگراف‌ها.

### `strip_diacritics(text: str) -> str`
حذف حرکات و اعراب (فتحه، ضمه، کسره، تنوین، تشدید، سکون).

### `is_persian(text: str) -> bool`
بررسی وجود حداقل یک کاراکتر از الفبای فارسی/عربی در متن.

### `clean_text(text: str, *, preserve_arabic: bool = False) -> str`
پالایش همه‌جانبه‌ی متن با محافظت از پیوندهای اینترنتی، آدرس‌های ایمیل، کدهای نرم‌افزاری و حذف نویسه‌های نامرئی یونیکد.

### `normalize_whitespace(text: str, keep_paragraphs: bool = True) -> str`
یکدست‌سازی انواع فاصله‌ها (فاصله‌های نازک، نیم‌فاصله‌های نامناسب، تب‌ها). در صورت `keep_paragraphs=False` تمامی خطوط به یک سطر ممتد تبدیل می‌گردند.

### `beautify_persian_spacing(text: str) -> str`
تنظیم فواصل استاندارد در اطراف علائم نگارشی (کامه «،»، نقطه‌ویرگول «؛»، گیومه ««»»، قوسین) با محافظت کامل از آدرس‌های وب، ایمیل‌ها و ارقام اعشاری.

### `smart_persian_spacing(text: str, preserve_urls: bool = True, preserve_quotes: bool = True) -> str`
تنظیم هوشمندانه‌ی نیم‌فاصله‌ها پیرامون پیشوندها و پسوندهای فعلی و اسمی با محافظت کامل از پیوندهای اینترنتی و نقل‌قول‌ها.

---

## چیدمان کیبورد و مرتب‌سازی الفبایی

### `correct_keyboard_layout(text: str, to: Literal["persian", "english", "auto"] = "persian", preserve_mixed: bool = False) -> str`
اصلاح دوطرفه‌ی کلماتی که با زبان اشتباه کیبورد تایپ شده‌اند:
- `to="persian"`: تبدیل کلیدهای لاتین به حروف دری/فارسی (مانند `"sghl"` به `"سلام"`).
- `to="english"`: تبدیل کلیدهای فارسی به معادل لاتین QWERTY (مانند `"اثممخ"` به `"hello"`).
- `to="auto"`: تشخیص خودکار جهت تبدیل.

### `expand_snippets(text: str, snippets: dict[str, str], word_boundary: bool = True) -> str`
گسترش خودکار اختصارات متنی به عبارات کامل (مثلاً `{"ق.ظ": "قبل از ظهر"}`).

### `persian_sort_key(s: str) -> tuple[int, ...]`
تولید کلید مرتب‌سازی الفبایی بر بنیاد ترتیب استاندارد الفبای فارسی.

### `persian_sorted(iterable: Iterable[T], *, reverse: bool = False) -> list[T]`
مرتب‌سازی الفبایی لستی از رشته‌ها بر بنیاد کلید بهینه‌شده.

---

## استخراج و تبدیل

### `normalize_digits(text: str, to: Literal["persian", "english", "arabic"] = "persian") -> str`
یکدست‌سازی ارقام متن به یکی از سیستم‌های عددی `"persian"`، `"english"`، یا `"arabic"`.

### `words_to_number(text: str) -> int`
تبدیل اعداد نوشته‌شده به حروف به ارقام عددی ریاضی (مانند تبدیل `"سی و دو هزار و پانصد"` به `32500`).

### `convert_numbers(text: str, to: Literal["persian", "english"] = "persian") -> str`
تبدیل ارقام موجود در متن میان دو خط لاتین و فارسی.

### `slugify(text: str, separator: str = "-") -> str`
تولید اسلاگ‌های معیاری انگلیسی بر مبنای واژه‌نامه‌ی ترانسکریپشن جهت استفاده در آدرس صفحات وب.

### `extract_mobiles(text: str) -> list[str]`
استخراج تمامی شماره‌های معتبر مبایل موجود در یک متن طولانی.

### `extract_national_codes(text: str) -> list[str]`
استخراج تمامی شناسه‌های ۱۰ رقمی معتبر از میان متن.

---

## پنهان‌سازی معلومات حساس (Masking)

### `mask_mobile(phone: str, mask_char: str = "*") -> str`
پنهان‌سازی ارقام میانی شماره‌ی مبایل (مانند `"0912***6789"`).

### `mask_card(card: str, mask_char: str = "*") -> str`
ماسک کردن بخش میانی کارت بانکی ۱۶ رقمی با حفظ گروه‌بندی ۴تایی.

### `mask_national_code(code: str, mask_char: str = "*") -> str`
پنهان‌سازی بخش میانی کود شناسایی.

### `mask_email(email: str, mask_char: str = "*") -> str`
پنهان‌سازی متناسب حروف نام کاربری در آدرس ایمیل.
