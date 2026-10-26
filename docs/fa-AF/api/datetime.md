# مرجع ماژول تاریخ و زمان (`parsikit.datetime`)

توابع تبدیل تقویم‌های هجری شمسی و میلادی، سنجش سال کبیسه و بیان زمان نسبی:

---

## توابع عمومی

### `gregorian_to_jalali(gy: int, gm: int, gd: int) -> tuple[int, int, int]`
تبدیل تاریخ میلادی (سال، ماه، روز) به تاریخ هجری شمسی (جلالی) با دقت محاسباتی نجومی.

### `jalali_to_gregorian(jy: int, jm: int, jd: int) -> tuple[int, int, int]`
تبدیل تاریخ هجری شمسی (سال، ماه، روز) به معادل میلادی.

### `is_jalali_leap(jy: int) -> bool`
بررسی ۳۶۶ روزه بودن (سال کبیسه) در گاهشماری هجری شمسی.

### `get_jalali_month_name(month: int) -> str`
بازگرداندن نام ماه هجری شمسی بر اساس شماره‌ی ماه (۱ تا ۱۲).

### `format_jalali(jy: int, jm: int, jd: int, pattern: str = "YYYY/MM/DD") -> str`
قالب‌بندی تاریخ هجری شمسی با استفاده از الگوی ورودی.

### `humanize_relative_time(dt_or_seconds, reference=None) -> str`
تبدیل تفاوت زمانی یا شیء `datetime` به عبارت متنی طبیعی همراه با ارقام فارسی (مانند `'هم‌اکنون'`, `'۱۵ دقیقه پیش'`, `'دیروز'`, `'در ۲ ساعت آینده'`).
