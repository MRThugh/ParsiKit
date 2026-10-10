"""
Invoice & Financial Calculations Demo with ParsiKit.
Demonstrates VAT calculations, words-to-currency, and loan installment planning.
"""
import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

import parsikit

def generate_invoice(item_name: str, base_amount_toman: int):
    # 1. Add VAT (Value Added Tax / ارزش افزوده)
    total_with_tax = parsikit.add_tax_and_toll(base_amount_toman, tax_rate=0.10)
    tax_amount = total_with_tax - base_amount_toman

    # 2. Convert to Rial
    total_rial = parsikit.toman_to_rial(total_with_tax)

    # 3. Format with Persian numerals and thousands separators
    formatted_base = parsikit.format_currency(base_amount_toman, "toman", persian_digits=True)
    formatted_tax = parsikit.format_currency(tax_amount, "toman", persian_digits=True)
    formatted_total = parsikit.format_currency(total_with_tax, "toman", persian_digits=True)

    # 4. Convert total to Persian words
    words_total = parsikit.format_currency_to_words(total_with_tax, "toman")

    print(f"=== صورتحساب: {item_name} ===")
    print(f"قیمت پایه: {formatted_base}")
    print(f"مالیات بر ارزش افزوده (۱۰٪): {formatted_tax}")
    print(f"مبلغ کل پرداختی: {formatted_total} ({total_rial:,} ریال)")
    print(f"مبلغ به حروف: {words_total}\n")

def main():
    generate_invoice("اشتراک سالانه نرم‌افزار", 12500000)

if __name__ == "__main__":
    main()
