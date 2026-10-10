"""
ParsiKit Quickstart Demonstration.
Demonstrates basic text processing, national code validation, and Persian numerals.
"""
import sys
from pathlib import Path

# Ensure project root is in path when executed directly
_ROOT = Path(__file__).resolve().parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

import parsikit

def main():
    print("=== ParsiKit Quickstart Demo ===\n")

    # 1. Standardize Persian text
    dirty_text = "ي كافيه كتاب ها رو برداري و بري"
    clean_text = parsikit.standardize_persian(dirty_text)
    print(f"Original: {dirty_text}")
    print(f"Standardized: {clean_text}\n")

    # 2. Iranian National Code (کد ملی)
    code = "7730123452"
    nc = parsikit.NationalCode(code)
    print(f"National Code: {nc.formatted} | Valid: {nc.is_valid} | Masked: {nc.masked}\n")

    # 3. Currency and Number Formatting
    price = 1500000
    words = parsikit.number_to_words(price)
    currency_str = parsikit.format_currency(price, "toman", persian_digits=True)
    print(f"Amount: {currency_str} ({words} تومان)\n")

    # 4. Jalali Dates
    jy, jm, jd = parsikit.gregorian_to_jalali(2026, 7, 6)
    month_name = parsikit.get_jalali_month_name(jm)
    print(f"Date: {parsikit.format_jalali(jy, jm, jd)} ({jd} {month_name} {jy})")

if __name__ == "__main__":
    main()
