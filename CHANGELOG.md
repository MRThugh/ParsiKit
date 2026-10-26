# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [3.3.1] - 2026-10-10

### Fixed
- **Terminal Color Detection & Windows Compatibility**: Replaced invalid `sys.environ` call with `os.environ` in `_supports_color()` (`parsikit/dev.py`) and added compliant support for `NO_COLOR`, `FORCE_COLOR`, Windows Terminal (`WT_SESSION`), ConEmu, and Windows 10+ ANSI console.
- **Zero-Padding in PersianFormatter**: Fixed visual width padding in `PersianFormatter` when formatting integers with zero-padding (e.g. `{:05d}`).
- **National Code Length Validation**: Enforced 8 to 10 digit boundary for Iranian national codes (up to 2 leading zeros omitted) in `is_valid_national_code`, rejecting under-length strings (such as `"27"`) and strings with letters or disallowed symbols.
- **Strict Character Sanitization in Validators**: Fixed `is_valid_mobile`, `is_valid_landline`, `is_valid_card_number`, `is_valid_postal_code`, `is_valid_sheba` to reject strings with unexpected alphabetic characters or symbols.
- **Domain Model Comparison**: Added rich comparison operators (`<, <=, >, >=`) to `StringLikeMixin` in `parsikit/models.py` allowing direct sorting with `sorted()`.
- **Non-Strict Property Fallbacks**: Prevented unhandled exceptions in `BankCard.formatted`, `BankCard.masked`, `Sheba.formatted`, `Sheba.account_number`, and `NationalCode.formatted` when initialized with `strict=False`.
- **Date Boundary Validation**: Added explicit month (1-12) and day (1-31) validation in `gregorian_to_jalali` and `jalali_to_gregorian` raising `ValueError` instead of unhandled `IndexError`.
- **Tax Breakdown Option**: Added `breakdown=False` optional parameter to `add_tax_and_toll` returning detailed breakdown dict `{"base", "tax", "rate", "total"}` when `breakdown=True`.
- **Python 3.10/3.11 Compatibility**: Resolved fatal `SyntaxError` in `parsikit/dev.py` caused by backslash expression in f-strings (PEP 701, which only applies to Python >=3.12).
- **Jalali Leap Year Calculation**: Fixed astronomical leap year calculation in `is_jalali_leap()` (`parsikit/datetime.py`) to align with the astronomical Solar Hijri cycle (e.g. 1399 and 1403 are leap years; 1400 and 1404 are normal years) and `jalali_to_gregorian`.
- **Postal Code Formatting Layout**: Corrected `format_postal_code()` in `parsikit/validators.py` from 3-6-1 (`XXX-XXXXXX-X`) to the official Iranian postal standard 5-5 layout (`XXXXX-XXXXX`).
- **Persian Formatter Grouping Separators**: Fixed `PersianFormatter` in `parsikit/dev.py` to localize thousand-grouping commas from ASCII `,` to Persian comma `،` when `:fa` or `:p` formatting specs are used.
- **Transliteration Dictionary (`slugify`)**: Added common Persian word `"نسخه": "neskheh"` to `_COMMON_WORDS_PINGLISH` in `parsikit/text.py`.
- **Relative Time Persian Numerals**: Fixed `humanize_relative_time()` in `parsikit/datetime.py` to format relative minute and hour counts using localized Persian digits rather than ASCII digits.
- **Text Inspection Numeral Detection**: Fixed `inspect_text()` in `parsikit/dev.py` to differentiate between ASCII Latin digits (`has_english_digits`) and Persian digits (`has_persian_digits`).
- **PII Security in Exceptions**: Sanitized `InvalidCardNumberError`, `InvalidNationalCodeError`, `InvalidMobileError`, and `InvalidShebaError` exception messages in `parsikit/models.py` to eliminate exposure of raw card numbers, national codes, and mobile numbers in exception messages and log traces.
- **Safe Masking Fallbacks**: Improved masking utilities (`mask_card`, `mask_mobile`, `mask_national_code`) to safely handle short or malformed inputs without leaking substrings.

### Added
- **Smart Typing & Cursor Preservation**: Implemented content-based relative cursor tracking in `parsikit/gui.py` (`_compute_text_cursor_pos` and `_compute_structured_cursor_pos`), eliminating cursor jumping during middle or end editing across Tkinter, CustomTkinter, and Qt (`QLineEdit`, `QTextEdit`, `QPlainTextEdit`).
- **Safe Unbinding**: Added `unbind_persian_input(widget)` for clean disconnection of event traces, listeners, and Qt signals.
- **Typing Options**: Added `digit_style`, `smart_spacing`, `snippets` dictionary expansion, and `enable_shortcuts` (Shift+Space for ZWNJ in Tkinter) to `bind_persian_input`.
- **Bidirectional Keyboard Layout Correction**: Enhanced `correct_keyboard_layout` with `to="persian"|"english"|"auto"`, reverse QWERTY mapping, CapsLock handling, and preservation of already-correct Persian.
- **Digits Normalization**: Added `normalize_digits` to convert digits across Latin, Persian, and Arabic-Indic Unicode blocks to a specified target script (`"persian"`, `"english"`, or `"arabic"`).
- **Smart Persian Spacing**: Added `smart_persian_spacing` with URL, email, and quotation protection.
- **Snippet Expansion**: Added `expand_snippets` with word boundary enforcement.
- **Persian Digits in format_jalali**: Added `persian_digits=True` option to `format_jalali`.
- **Masked Property on Models**: Added `.masked` property to `BankCard`, `MobileNumber`, and `NationalCode` domain models for safe logging and administration interfaces.
- **Reorganized Modular Test Suite**: Structured automated tests into `tests/unit/`, `tests/integration/`, `tests/regression/`, `tests/security/`, and `tests/fixtures/`.
- **Synthetic Test Fixtures**: Created `tests/fixtures/synthetic_data.py` providing valid synthetic test fixtures that do not expose real customer PII.
- **Bilingual Documentation**: Comprehensive, navigable documentation across 4 languages (`en`, `fa`, `fa-AF`, `tg`), including tutorials, guides, and complete API references.
- **Runnable Examples**: Standalone educational demonstrations in canonical `examples/` directory.
- **Continuous Integration**: Added GitHub Actions workflow (`.github/workflows/ci.yml`) testing Python 3.10, 3.11, 3.12, and 3.13.

---

## [3.3.0] - 2026-04-12

### Added
- **Developer Utilities & Diagnostics**: Added `parsikit.dev` with `pformat`, `persian_fstring`, `inspect_text`, `debug_text`, and `validate_batch`.
- **Visual Width Awareness**: Visual length calculation accounting for Zero-Width Non-Joiners (ZWNJ) and Arabic diacritics.
- **Thread-Safe Caching**: Introduced `parsikit.cache` thread-safe LRU-like cache for expensive number-to-words transformations.
- **Centralized Configuration**: Added `parsikit.config` (`ParsiKitConfig`) to configure default tax rates, default currencies, and caching.
- **Object-Oriented Domain Models**: Added `PersianText`, `NationalCode`, `MobileNumber`, `FixedLine`, `BankCard`, `Sheba`, and `VehiclePlate` with native Pydantic v2 support.
- **Sensitive Data Masking**: Added `mask_mobile`, `mask_card`, `mask_national_code`, and `mask_email`.
- **Smart Data Classifier**: Added `detect()` utility in `parsikit.validators`.

---

## [3.2.0] - 2025-11-05

### Added
- Currency conversion utilities (`rial_to_toman`, `toman_to_rial`).
- Formatted currency string generators with Persian digits (`format_currency`).
- Value-Added Tax (VAT) computation (`add_tax_and_toll`).
- Loan installment amortization calculations (`calculate_installments`).

---

## [3.1.0] - 2025-08-20

### Added
- Astronomical Solar Hijri (Jalali) to Gregorian conversions (`gregorian_to_jalali`, `jalali_to_gregorian`).
- Jalali month name lookups and leap year detection.
- Persian relative-time humanization (`humanize_relative_time`).
- Words-to-number parser (`words_to_number`).

---

## [3.0.0] - 2025-05-15

### Added
- Initial unified architecture for ParsiKit Persian text processing, national code validation, and telephone number handling.
