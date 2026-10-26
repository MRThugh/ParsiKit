# Datetime API (`parsikit.datetime`)

## Functions

### `gregorian_to_jalali(gy: int, gm: int, gd: int) -> tuple[int, int, int]`
Converts a Gregorian date (year, month, day) to the astronomical Solar Hijri (Jalali) date. Validates month (1–12) and day (1–31), raising `ValueError` for invalid boundaries.

### `jalali_to_gregorian(jy: int, jm: int, jd: int) -> tuple[int, int, int]`
Converts a Jalali date (year, month, day) to the corresponding Gregorian date. Validates month (1–12) and day (1–31), raising `ValueError` for invalid boundaries.

### `is_jalali_leap(jy: int) -> bool`
Determines whether a Jalali year is a 366-day leap year using the astronomical solar cycle.

### `get_jalali_month_name(month: int) -> str`
Returns the Persian name of the month (1 = فروردین, ..., 12 = اسفند).

### `format_jalali(jy: int, jm: int, jd: int, pattern: str = "YYYY/MM/DD", *, persian_digits: bool = False) -> str`
Formats a Jalali date using the given pattern. When `persian_digits=True`, formats output digits as Persian numerals (e.g. `'۱۴۰۵/۰۴/۱۵'`).

### `humanize_relative_time(dt_or_seconds, reference=None) -> str`
Translates a `datetime` object or time difference into natural Persian words with Persian digits (e.g. `'هم‌اکنون'`, `'۱۵ دقیقه پیش'`, `'دیروز'`, `'در ۲ ساعت آینده'`).
