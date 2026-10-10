"""
Jalali Dates & Relative Time Humanization Demo with ParsiKit.
"""
import datetime
import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

import parsikit

def main():
    print("=== نمایش تاریخ شمسی و زمان نسبی در پارسی‌کیت ===\n")

    # Current reference point
    now = datetime.datetime.now()

    timestamps = [
        ("لحظاتی قبل", now - datetime.timedelta(seconds=5)),
        ("چند دقیقه پیش", now - datetime.timedelta(minutes=15)),
        ("چند ساعت پیش", now - datetime.timedelta(hours=4)),
        ("دیروز", now - datetime.timedelta(days=1)),
        ("چند روز قبل", now - datetime.timedelta(days=6)),
    ]

    for label, dt in timestamps:
        humanized = parsikit.humanize_relative_time(dt, reference=now)
        print(f"{label:<15}: {humanized}")

    # Jalali month details
    jy, jm, jd = parsikit.gregorian_to_jalali(now.year, now.month, now.day)
    is_leap = parsikit.is_jalali_leap(jy)
    month_name = parsikit.get_jalali_month_name(jm)
    print(f"\nامروز: {jd} {month_name} {jy} (سال {'کبیسه است' if is_leap else 'کبیسه نیست'})")

if __name__ == "__main__":
    main()
