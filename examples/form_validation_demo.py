"""
Form Validation and Entity Parsing Demo with ParsiKit.
Shows how to validate web form submissions securely.
"""
import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

import parsikit

def validate_user_registration(form_data: dict):
    print("--- Processing Registration Form ---")
    results = {}

    # Validate National Code
    try:
        nc = parsikit.NationalCode(form_data.get("national_code", ""))
        results["national_code"] = {
            "valid": True,
            "formatted": nc.formatted,
            "masked": nc.masked,
            "location": nc.location,
        }
    except parsikit.InvalidNationalCodeError as e:
        results["national_code"] = {"valid": False, "error": str(e)}

    # Validate Mobile Number
    try:
        mob = parsikit.MobileNumber(form_data.get("mobile", ""))
        results["mobile"] = {
            "valid": True,
            "national": mob.to_national(),
            "international": mob.to_international(),
            "operator": mob.operator,
            "masked": mob.masked,
        }
    except parsikit.InvalidMobileError as e:
        results["mobile"] = {"valid": False, "error": str(e)}

    # Validate Bank Card
    try:
        card = parsikit.BankCard(form_data.get("card", ""))
        results["card"] = {
            "valid": True,
            "formatted": card.formatted,
            "bank": card.bank["name"] if card.bank else "نامشخص",
            "masked": card.masked,
        }
    except parsikit.InvalidCardNumberError as e:
        results["card"] = {"valid": False, "error": str(e)}

    return results

def main():
    sample_valid_form = {
        "national_code": "0010123458",
        "mobile": "+989123456789",
        "card": "6037991122334455",
    }
    outcome = validate_user_registration(sample_valid_form)
    for field, data in outcome.items():
        print(f"{field}: {data}")

if __name__ == "__main__":
    main()
