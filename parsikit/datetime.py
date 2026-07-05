"""
parsikit.datetime
~~~~~~~~~~~~~~~~~
Zero-dependency, high-precision astronomical date conversion utilities 
between Gregorian and Jalali (Shamsi) calendars.
"""


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