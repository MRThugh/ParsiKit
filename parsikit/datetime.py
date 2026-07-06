"""
parsikit.datetime
~~~~~~~~~~~~~~~~~
Zero-dependency, high-precision astronomical date conversion utilities 
between Gregorian and Jalali (Shamsi) calendars.
"""

from __future__ import annotations
import datetime
from parsikit.cache import memoize

_JALALI_MONTH_NAMES = [
    "فروردین", "اردیبهشت", "خرداد", "تیر", "مرداد", "شهریور",
    "مهر", "آبان", "آذر", "دی", "بهمن", "اسفند"
]


@memoize(maxsize=4096)
def gregorian_to_jalali(gy: int, gm: int, gd: int) -> tuple[int, int, int]:
    """Convert a Gregorian date (Year, Month, Day) to Jalali (Shamsi) date."""
    g_d_m = [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 335]
    if (gy % 4 == 0 and gy % 100 != 0) or (gy % 400 == 0):
        leap = 1
    else:
        leap = 0
    
    gy2 = gy - 1600
    gm2 = gm - 1
    gd2 = gd - 1
    
    g_day_no = 365 * gy2 + (gy2 + 3) // 4 - (gy2 + 99) // 100 + (gy2 + 399) // 400
    
    for i in range(gm2):
        g_day_no += g_d_m[i + 1] - g_d_m[i]
    if gm2 > 1 and leap:
        g_day_no += 1
    g_day_no += gd2
    
    j_day_no = g_day_no - 79
    
    j_np = j_day_no // 12053
    j_day_no %= 12053
    
    jy = 979 + 33 * j_np + 4 * (j_day_no // 1461)
    j_day_no %= 1461
    
    if j_day_no >= 366:
        jy += (j_day_no - 1) // 365
        j_day_no = (j_day_no - 1) % 365
        
    for i in range(11):
        if j_day_no < (31 if i < 6 else 30):
            jm = i + 1
            jd = j_day_no + 1
            return jy, jm, jd
        j_day_no -= 31 if i < 6 else 30
    jm = 12
    jd = j_day_no + 1
    return jy, jm, jd


@memoize(maxsize=4096)
def jalali_to_gregorian(jy: int, jm: int, jd: int) -> tuple[int, int, int]:
    """Convert a Jalali (Shamsi) date (Year, Month, Day) to Gregorian date."""
    jy2 = jy - 979
    jm2 = jm - 1
    jd2 = jd - 1
    
    j_day_no = 365 * jy2 + (jy2 // 33) * 8 + (jy2 % 33 + 3) // 4
    for i in range(jm2):
        j_day_no += 31 if i < 6 else 30
    j_day_no += jd2
    
    g_day_no = j_day_no + 79
    
    gy = 1600 + 400 * (g_day_no // 146097)
    g_day_no %= 146097
    
    leap = 1
    if g_day_no >= 36525:
        g_day_no -= 1
        gy += 100 * (g_day_no // 36524)
        g_day_no %= 36524
        if g_day_no >= 365:
            g_day_no += 1
        else:
            leap = 0
            
    gy += 4 * (g_day_no // 1461)
    g_day_no %= 1461
    
    if g_day_no >= 366:
        leap = 0
        g_day_no -= 1
        gy += g_day_no // 365
        g_day_no %= 365
        
    g_d_m = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    if leap:
        g_d_m[2] = 29
        
    for i in range(12):
        if g_day_no < g_d_m[i + 1]:
            gm = i + 1
            gd = g_day_no + 1
            return gy, gm, gd
        g_day_no -= g_d_m[i + 1]
    return gy, 12, 31


def format_jalali(jy: int, jm: int, jd: int, pattern: str = "YYYY/MM/DD") -> str:
    """Format a Jalali date into a readable string pattern (e.g., YYYY/MM/DD, YYYY-MM-DD)."""
    y_str = str(jy).zfill(4)
    m_str = str(jm).zfill(2)
    d_str = str(jd).zfill(2)
    return pattern.replace("YYYY", y_str).replace("MM", m_str).replace("DD", d_str)


def get_jalali_month_name(month: int) -> str:
    """Get the Persian name of a Jalali month (1 to 12)."""
    if not (1 <= month <= 12):
        raise ValueError("Month must be between 1 and 12.")
    return _JALALI_MONTH_NAMES[month - 1]


def is_jalali_leap(jy: int) -> bool:
    """Determine if a Jalali year is a leap (Kabiseh) year (astronomical 2820-year cycle)."""
    epbase = jy - 474 if jy > 0 else jy - 473
    epyear = 474 + (epbase % 2820)
    return ((epyear * 682) % 2816) < 682


def humanize_relative_time(
    dt_or_seconds: datetime.datetime | float,
    reference: datetime.datetime | None = None,
) -> str:
    """Convert a datetime or a timestamp into a friendly human-readable relative time string in Persian.
    
    E.g. "۳ دقیقه پیش", "دیروز", "۱ سال قبل", "فردا", "هم‌اکنون".
    """
    if reference is None:
        reference = datetime.datetime.now()

    if isinstance(dt_or_seconds, (int, float)):
        dt = datetime.datetime.fromtimestamp(dt_or_seconds)
    else:
        dt = dt_or_seconds

    diff = reference - dt
    seconds = diff.total_seconds()
    is_past = seconds >= 0
    abs_seconds = abs(seconds)

    if abs_seconds < 10:
        return "هم‌اکنون" if is_past else "چند ثانیه بعد"
    elif abs_seconds < 60:
        val = int(abs_seconds)
        suffix = "پیش" if is_past else "بعد"
        return f"{val} ثانیه {suffix}"
    elif abs_seconds < 3600:
        val = int(abs_seconds // 60)
        suffix = "پیش" if is_past else "بعد"
        return f"{val} دقیقه {suffix}"
    elif abs_seconds < 86400:
        val = int(abs_seconds // 3600)
        suffix = "پیش" if is_past else "بعد"
        if val == 1:
            return "۱ ساعت پیش" if is_past else "۱ ساعت بعد"
        return f"{val} ساعت {suffix}"
    elif abs_seconds < 172800:
        if is_past:
            return "دیروز"
        return "فردا"
    elif abs_seconds < 2592000:
        val = int(abs_seconds // 86400)
        suffix = "پیش" if is_past else "بعد"
        return f"{val} روز {suffix}"
    elif abs_seconds < 31104000:
        val = int(abs_seconds // 2592000)
        suffix = "پیش" if is_past else "بعد"
        if val == 1:
            return "۱ ماه پیش" if is_past else "۱ ماه بعد"
        return f"{val} ماه {suffix}"
    else:
        val = int(abs_seconds // 31104000)
        suffix = "قبل" if is_past else "بعد"
        if val == 1:
            return "۱ سال قبل" if is_past else "۱ سال بعد"
        return f"{val} سال {suffix}"