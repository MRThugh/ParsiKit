# Guide: Form Validation & Sensitive Data Security

Handling Personally Identifiable Information (PII) such as national identification numbers, credit card numbers, and phone numbers requires strict security controls to prevent exposure in application logs, APM systems, and customer service dashboards.

---

## 1. Input Sanitization Before Storage

Always sanitize text input from web forms before storing it in databases:

```python
import parsikit

def sanitize_user_input(raw_full_name: str, raw_address: str):
    return {
        "full_name": parsikit.clean_text(raw_full_name),
        "address": parsikit.beautify_persian_spacing(parsikit.clean_text(raw_address)),
    }
```

---

## 2. Preventing PII Leakage in Logs

When logging user transactions, NEVER log raw card numbers or national codes. Use the `.masked` property or `mask_*` functions:

```python
import logging
import parsikit

logger = logging.getLogger("payment")

def process_payment(card_number_raw: str, national_code_raw: str):
    card = parsikit.BankCard(card_number_raw)
    nc = parsikit.NationalCode(national_code_raw)

    # SECURE: Log only masked representations
    logger.info(
        "Initiating payment for user (National Code: %s) using Card: %s (%s)",
        nc.masked,
        card.masked,
        card.bank_name,
    )
```

---

## 3. Safe Exception Handling

In ParsiKit v3.3.1, exceptions like `InvalidCardNumberError` and `InvalidNationalCodeError` are sanitized by default so they do not print the raw secret card number into stack traces or Sentry events.

```python
import parsikit

try:
    card = parsikit.BankCard("6037991122339999")  # Invalid Luhn
except parsikit.InvalidCardNumberError as exc:
    # exc message is safe and contains no sensitive PII
    logger.warning("Payment validation failed: %s", exc)
```
