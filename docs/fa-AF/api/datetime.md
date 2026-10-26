# مرجع ماژول تاریخ و زمان (`parsikit.datetime`)

توابع تبدیل تقویم‌های هجری شمسی و میلادی، سنجش سال کبیسه و بیان زمان نسبی:

---

## توابع عمومی

### `gregorian_to_jalali(gy: int, gm: int, gd: int) -> tuple[int, int, int]`
تبدیل تاریخ میلادی (سال، ماه، روز) به تاریخ هجری شمسی (جلالی) با دقت محاسباتی نجومی. ورودی‌های ماه (۱ تا ۱۲) و روز (۱ تا ۳۱) اعتبارسنجی شده و در صورت عدم تطابق `ValueError` صادر می‌شود.

### `jalali_to_gregorian(jy: int, jm: int, jd: int) -> tuple[int, int, int]`
تبدیل تاریخ هجری شمسی (سال، ماه، روز) به معادل میلادی با ارزیابی محدوده‌ی معتبر ماه و روز.

### `is_jalali_leap(jy: int) -> bool`
بررسی ۳۶۶ روزه بودن (سال کبیسه) در گاهشماری هجری شمسی.

### `get_jalali_month_name(month: int) -> str`
بازگرداندن نام ماه هجری شمسی بر اساس شماره‌ی ماه (۱ تا ۱۲).

### `format_jalali(jy: int, jm: int, jd: int, pattern: str = "YYYY/MM/DD", *, persian_digits: bool = False) -> str`
قالب‌بندی تاریخ هجری شمسی با استفاده از الگوی ورودی (با گزینه‌ی `persian_digits=True` جهت درج ارقام به رسم‌الخط فارسی).

### `humanize_relative_time(dt_or_seconds, reference=None) -> str`
تبدیل تفاوت زمانی یا شیء `datetime` به عبارت متنی طبیعی همراه با ارقام فارسی (مانند `'هم‌اکنون'`, `'۱۵ دقیقه پیش'`, `'دیروز'`, `'در ۲ ساعت آینده'`).
