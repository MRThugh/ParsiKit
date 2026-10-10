# ParsiKit Official Documentation (v3.3.1)

Welcome to the official documentation for **ParsiKit**!  
Created and maintained by **Ali Kamrani (MRThugh)**, ParsiKit is a pure Python software infrastructure library designed for Persian data standardization, validation algorithms, financial computations, astronomical Jalali calendar transformations, graphical font reshaping, developer diagnostics, and sensitive data protection.

---

## What is ParsiKit?

ParsiKit solves standard challenges encountered when handling Persian text and Iranian data in Python:
- **Text & Typography Standardization**: Converts Arabic letters (ي/ك/ة) to standard Persian glyphs, correctly positions Zero-Width Non-Joiners (ZWNJ) for prefixes (`می‌`) and suffixes (`‌ها`), eliminates redundant whitespace, and strips diacritics.
- **Official National Validations**: Checks mathematical checksum algorithms for Iranian National Codes (modulo 11), 16-digit debit/credit card numbers (Luhn check), Sheba IBANs (ISO 7064 Mod 97-10), mobile phones, fixed landlines, corporate IDs, postal codes, bills, and vehicle plates.
- **Numbers & Currencies**: Translates numerals between Persian, Arabic, and Latin scripts, converts huge numbers into Persian words, performs Rial and Toman conversions, computes VAT, and calculates loan installments.
- **Astronomical Jalali Dates**: Bidirectional date conversions between Gregorian and Jalali calendars with leap year validation and relative-time humanization.
- **Object-Oriented Domain Models**: Rich value objects (`PersianText`, `NationalCode`, `MobileNumber`, `BankCard`, `Sheba`, `VehiclePlate`) with instant validation, masked views, and native Pydantic v2 support.
- **Security & Privacy**: Masking helpers (`mask_card`, `mask_mobile`, `mask_national_code`, `mask_email`) and sanitized exceptions to prevent PII exposure in logs and metrics.
- **Zero External Dependencies**: Pure Python, zero compile steps, minimal memory footprint.

---

## What ParsiKit Does NOT Do

1. **Identity Inquiries (Registration Office / Civil Registry)**:  
   `is_valid_national_code` mathematically verifies length and checksum against the official algorithm. It does not call an online governmental web service to verify the person's identity or living status.
2. **Bank Balance or Live Account Status**:  
   `BankCard` and `Sheba` verify format, check digits, and issuer bank identity. They do not connect to banking APIs to check available balance or card blocking status.

---

## Documentation Navigation

- 🚀 **[Installation](installation.md)** — Install via pip or from source.
- ⚡ **[Quickstart](quickstart.md)** — Practical examples in 5 minutes.
- 📚 **Step-by-Step Tutorials:**
  - [Text Processing & ZWNJ](tutorials/text_processing.md)
  - [Validation & Checksums](tutorials/validation.md)
  - [Numbers & Financial Operations](tutorials/numbers_and_currency.md)
  - [Jalali Calendar & Humanized Time](tutorials/datetime.md)
  - [Object-Oriented Models & Pydantic](tutorials/models.md)
- 🛠 **Guides:**
  - [Web Backends (FastAPI & Django)](guides/web_backends.md)
  - [Forms & Security Best Practices](guides/forms_and_security.md)
  - [GUI Integration (Tkinter, CustomTkinter, Graphics)](guides/gui_integration.md)
- 📖 **[API Reference](api/index.md)** — Complete module and function reference.
- 🔧 **[Troubleshooting](troubleshooting.md)** — Solutions to common issues.
- ❓ **[FAQ](faq.md)** — Frequently Asked Questions.
