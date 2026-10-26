# مرجع توابع تاریخ جلالی و زمان نسبی (`parsikit.datetime`)

ماژول `parsikit.datetime` ابزارهای دقیق محاسبات تقویم هجری شمسی (جلالی) و تبدیل آن به گاه‌شماری میلادی را بدون نیاز به وابستگی خارجی فراهم می‌سازد.

---

## ۱. تبدیل تقویم‌ها

### `gregorian_to_jalali(gy: int, gm: int, gd: int) -> tuple[int, int, int]`
تاریخ میلادی (سال، ماه، روز) را با دقت بالا به تاریخ هجری شمسی (سال، ماه، روز) تبدیل می‌کند. ورودی‌های ماه (۱ تا ۱۲) و روز (۱ تا ۳۱) به طور دقیق اعتبارسنجی شده و در صورت خروج از محدوده، خطای `ValueError` صادر می‌شود.

```python
import parsikit

jy, jm, jd = parsikit.gregorian_to_jalali(2026, 7, 6)
print(jy, jm, jd)  # (1405, 4, 15)
```

### `jalali_to_gregorian(jy: int, jm: int, jd: int) -> tuple[int, int, int]`
تاریخ هجری شمسی را به تاریخ میلادی متناظر تبدیل می‌کند. در صورت مقادیر نامعتبر ماه یا روز خطای `ValueError` ایجاد می‌گردد.

```python
gy, gm, gd = parsikit.jalali_to_gregorian(1405, 4, 15)
print(gy, gm, gd)  # (2026, 7, 6)
```

---

## ۲. بررسی سال کبیسه و اسامی ماه‌ها

### `is_jalali_leap(jy: int) -> bool`
بررسی می‌کند که آیا سال شمسی مشخص‌شده کبیسه (۳۶۶ روزه با ۳۰ روز در ماه اسفند) است یا خیر. محاسبات منطبق بر دوره‌های سال‌شماری خورشیدی است.

```python
print(parsikit.is_jalali_leap(1399))  # True
print(parsikit.is_jalali_leap(1400))  # False
print(parsikit.is_jalali_leap(1403))  # True
```

### `get_jalali_month_name(month: int) -> str`
نام فارسی ماه شمسی را برمی‌گرداند (۱: فروردین، ...، ۱۲: اسفند).

### `format_jalali(jy: int, jm: int, jd: int, pattern: str = "YYYY/MM/DD", *, persian_digits: bool = False) -> str`
تاریخ شمسی را در قالب رشته‌ای با الگوی مورد نظر فرمت می‌کند. با فعال‌سازی `persian_digits=True`، ارقام به صورت فارسی درج می‌شوند (مانند `'۱۴۰۵/۰۴/۱۵'`).

---

## ۳. نمایش زمان نسبی فارسی (`humanize_relative_time`)

### `humanize_relative_time(dt_or_seconds, reference=None) -> str`
یک شیء زمان (`datetime`) یا فاصله زمانی بر حسب ثانیه را به عبارت خوانا و محاوره‌ای فارسی تبدیل می‌کند (با اعداد فارسی):

- `هم‌اکنون`
- `۱۵ دقیقه پیش` / `در ۱۵ دقیقه آینده`
- `۳ ساعت پیش` / `در ۳ ساعت آینده`
- `دیروز` / `فردا`
- `۵ روز پیش`
- `۲ ماه پیش`
- `۳ سال پیش`
