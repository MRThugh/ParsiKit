# ParsiKit v3.3.1 — Phase Zero Baseline Audit Report

**Author & Project Owner:** Ali Kamrani (MRThugh)  
**Auditor:** ParsiKit QA & Release Engineering Team  
**Audit Date:** 2026-10-10  
**Environment:** Linux (x86_64), Python 3.10.12 (GCC 11.4.0)  
**Target Release:** v3.3.1 (Patch Release from v3.3.0)

---

## 1. Executive Summary

This audit report documents the baseline state of the **ParsiKit** repository immediately following import.
ParsiKit is a pure Python library providing Persian data infrastructure: text standardization, typography, national validation algorithms (National Code, Mobile, Sheba, Bank Card, License Plates, Postal Codes, Bills), Jalali astronomical date utilities, currency calculations, rich domain models, and developer tools.

During the Phase Zero baseline inspection, several critical findings were discovered:
1. **Import Failure on Supported Python Versions (Python 3.10 / 3.11):**
   `pyproject.toml` and `setup.py` both claim `requires-python = ">=3.10"`. However, importing `parsikit` on Python 3.10 failed with a fatal `SyntaxError` in `parsikit/dev.py` line 366 due to backslash usage inside an f-string expression (PEP 701, only supported in Python >=3.12).
2. **Initial Test Suite Failures (7 Failures, 2 Errors):**
   Once the syntax error was addressed, executing the existing test suite (`test.py`) revealed 9 test issues:
   - **National code checksum mismatch in test fixture:** Test used `0010123451` as a sample valid code, but mathematically its modulo-11 check digit is `8` (`0010123458`). This caused 2 errors (`test_national_code_model`, `test_string_like_behavior_and_duck_typing`) and 1 failure (`test_validate_batch`).
   - **Visual alignment and zero-width non-joiner (ZWNJ):** Test input `"کتاب‌‌ها"` contained accidental duplicate ZWNJs (`\u200C\u200C`), causing visual length calculation discrepancies in `pformat`.
   - **Thousand grouping separator with Persian digits:** `PersianFormatter` formatted thousand-separated numbers with ASCII commas (e.g. `۱۵,۰۰۰`) instead of standard Persian commas (`۱۵،۰۰۰`), failing `test_persian_fstring_capturing`.
   - **Pinglish dictionary omission:** The word `"نسخه"` ("neskheh") was missing from `_COMMON_WORDS_PINGLISH`, causing fallback to character-by-character transliteration `nskhh` and failing `test_slugify`.
   - **Relative time formatting numerals:** `humanize_relative_time` used ASCII numerals in several branches (e.g. `5 دقیقه پیش`) rather than Persian numerals (`۵ دقیقه پیش`), failing `test_humanize_relative_time`.
   - **Email masking discrepancy:** `mask_email("kamrani.exe@gmail.com")` produced 8 asterisks (`ka********e@gmail.com`) due to 1-to-1 character masking of the 8 middle characters (`mrani.ex`), while the test expected 6 asterisks (`ka******e@gmail.com`) due to an eyeballed fixture count.
   - **Numeral detection in text inspection:** `test_inspect_text` asserted `has_english_digits` on `"ي كافيه ك کتاب ها ميباشد ۱۲۳"`, which contained Persian numerals (`۱۲۳`) rather than English numerals (`123`).
3. **Subtle Algorithmic and Structural Defects Found:**
   - **Jalali Leap Year Calculation Off-by-One:** `is_jalali_leap()` returned `False` for real astronomical leap years (e.g. 1399, 1403) and `True` for non-leap years (1400, 1404), while `jalali_to_gregorian` handled leap days correctly.
   - **Postal Code Formatting Copy-Paste Bug:** `format_postal_code` formatted 10-digit postal codes as `XXX-XXXXXX-X` (the 3-6-1 national code layout) rather than `XXXXX-XXXXX` (5-5 layout) as described in its docstring and Iranian postal specifications.
4. **Packaging and Build Environment:**
   No build/packaging tools were pre-installed in the bare Python environment.

---

## 2. Environment and Baseline Test Run

### Command
```bash
python3 test.py
```

### Initial Run Output (Prior to Fixes)
```text
Traceback (most recent call last):
  File "/app/applet/test.py", line 8, in <module>
    import parsikit
  File "/app/applet/parsikit/__init__.py", line 47, in <module>
    from .dev import (
  File "/app/applet/parsikit/dev.py", line 366
    print(f"  Raw Text: {colored(f'\"{text}\"', COLOR_GREEN)}")
                                                              ^
SyntaxError: f-string expression part cannot include a backslash
```

### Secondary Run Output (After dev.py syntax fix, running original test.py)
```text
Ran 23 tests in 0.019s
FAILED (failures=7, errors=2)
Passed: 14 / 23
```

Detailed failure breakdown:
| Test Name | Status | Root Cause |
|---|---|---|
| `test_string_like_behavior_and_duck_typing` | ERROR | Fixture `0010123451` has invalid check digit (expected `8`) |
| `test_national_code_model` | ERROR | Same invalid fixture `0010123451` |
| `test_validate_batch` | FAIL | Batch expects 2 valid codes, but fixture `0010123451` failed validation |
| `test_inspect_text` | FAIL | Text had Persian digits `۱۲۳`, test asserted `has_english_digits` |
| `test_mask_utilities` | FAIL | `mask_email` 8 masked chars vs test expecting 6 stars |
| `test_persian_fstring_capturing` | FAIL | ASCII comma `,` instead of Persian comma `،` in `:,fa` spec |
| `test_pformat_and_persian_aware_alignment` | FAIL | Accidental double ZWNJ `\u200C\u200C` in `"کتاب‌‌ها"` |
| `test_slugify` | FAIL | `"نسخه"` missing in Pinglish dictionary, producing `nskhh` |
| `test_humanize_relative_time` | FAIL | Format string used raw int instead of `english_to_persian` |

---

## 3. Inventory of Public Modules and APIs

The public API is exposed from `parsikit/__init__.py` and defined in 11 core modules:

### 1. Configuration & Exceptions
- `parsikit.config`: `ParsiKitConfig` instance managing `default_tax_rate`, `default_currency`, `enable_cache`.
- `parsikit.exceptions`: `ParsiKitError`, `ValidationError`, `InvalidNationalCodeError`, `InvalidMobileError`, `InvalidCardNumberError`, `InvalidShebaError`, `InvalidPostalCodeError`, `InvalidPlateError`, `InvalidBillError`.

### 2. Domain Models (`parsikit.models`)
- `PersianText`: Rich text model supporting standardization, diacritic stripping, keyboard layout correction, entity extraction, and word-to-number parsing.
- `NationalCode`: Value object with loose/strict validation, formatting (`XXX-XXXXXX-X`), and location detection.
- `MobileNumber`: Iranian mobile representation with national (`09...`) and international (`+989...`) formatting and operator detection.
- `FixedLine`: Fixed landline telephone model with province and area code detection.
- `BankCard`: 16-digit debit/credit card model with Luhn check, bank identification, and chunk formatting.
- `Sheba`: IBAN representation with check digit validation, bank identification, and clean account extraction.
- `VehiclePlate`: Iranian vehicle plate model with category and province parsing.

### 3. Text Processing (`parsikit.text`)
- `standardize_persian(text, *, strip_diacritics_opt=False)`: Standardizes Arabic characters (ي/ك/ة), ZWNJ prefixes/suffixes, and redundant whitespace.
- `strip_diacritics(text)`: Removes Arabic/Persian diacritics.
- `is_persian(text)`: Checks if string contains Persian/Arabic characters.
- `correct_keyboard_layout(text)`: Converts mistyped English layout text to Persian.
- `persian_sort_key(s)`: Alphabetical sorting key matching Persian collation.
- `persian_sorted(iterable, *, reverse=False)`: Persian alphabetical sort.
- `beautify_persian_spacing(text)`: Punctuation spacing and parenthesis balancing.
- `extract_mobiles(text)`: Regex extraction and validation of mobile numbers.
- `extract_national_codes(text)`: Regex extraction and checksum validation of national codes.
- `words_to_number(text)`: Parses written Persian words (e.g. "سی و دو هزار") into integers.
- `slugify(text, separator="-")`: Generates SEO-friendly Finglish URL slugs.
- `clean_text(text)`: Comprehensive text cleaner.
- `normalize_whitespace(text, keep_paragraphs=True)`: Standardizes spacing and newlines.
- `convert_numbers(text, to="persian")`: Bidirectional digit script translation.
- `mask_mobile(phone, mask_char="*")`: Masks mobile numbers (`0912***6789`).
- `mask_card(card, mask_char="*")`: Masks card numbers (`6037-99**-****-4455`).
- `mask_national_code(code, mask_char="*")`: Masks national codes (`773-****45-2`).
- `mask_email(email, mask_char="*")`: Masks email usernames.

### 4. Numbers & Currency (`parsikit.number`, `parsikit.currency`)
- `english_to_persian(text)`, `persian_to_english(text)`: Digit translation tables.
- `number_to_words(number)`: Converts integers up to 999 septillion into written Persian words.
- `format_currency(amount, currency=None, *, persian_digits=False)`: Formats amounts with labels (تومان / ریال).
- `rial_to_toman(amount)`, `toman_to_rial(amount)`: Rial <-> Toman conversion.
- `format_currency_to_words(amount, currency=None)`: Written Persian currency strings.
- `add_tax_and_toll(amount, tax_rate=None)`: VAT calculation.
- `calculate_installments(principal, annual_interest_rate, months)`: Monthly loan amortization.

### 5. Validation & Parsing (`parsikit.validators`)
- `is_valid_national_code`, `format_national_code`, `detect_national_code_location`
- `is_valid_mobile`, `normalize_mobile`, `detect_mobile_operator`
- `is_valid_landline`, `normalize_landline`, `detect_landline_province`
- `is_valid_card_number`, `format_card_number`, `detect_bank_from_card`
- `is_valid_sheba`, `format_sheba`, `detect_bank_from_sheba`, `extract_account_number_from_sheba`
- `is_valid_corporate_id`: 11-digit legal entity validation.
- `is_valid_postal_code`, `format_postal_code`
- `is_valid_bill_and_payment`, `extract_bill_details`
- `is_valid_plate`, `parse_plate`, `format_plate`
- `detect(text)`: Auto-detection of data type.

### 6. Datetime (`parsikit.datetime`)
- `gregorian_to_jalali(gy, gm, gd)`: Gregorian to Jalali astronomical date conversion.
- `jalali_to_gregorian(jy, jm, jd)`: Jalali to Gregorian date conversion.
- `format_jalali(jy, jm, jd, pattern="YYYY/MM/DD")`: Jalali string formatting.
- `get_jalali_month_name(month)`: Persian month name.
- `is_jalali_leap(jy)`: Jalali leap year check.
- `humanize_relative_time(dt_or_seconds, reference=None)`: Friendly relative time in Persian.

### 7. Reshaping & GUI (`parsikit.reshaper`, `parsikit.gui`)
- `reshape_for_graphics(text, reverse=True)`: Persian letter shaping & BiDi reversal for graphics engines.
- `reshape_paragraph_for_graphics(text, max_chars_per_line, reverse=True)`: Multi-line wrapped shaping.
- `bind_persian_input(widget, input_type="text")`: Live typing assistant for Tkinter/CustomTkinter/Qt.

### 8. Developer Tools (`parsikit.dev`)
- `inspect_text(text)`: Structural layout and typography diagnostics.
- `debug_text(text)`: Colored terminal diagnostics report.
- `validate_batch(items, model_class, silent=False)`: Batch evaluation of domain models.
- `persian_repr(obj)`: Unicode-preserving string representation.
- `setup_logging(level="INFO")`: Configures Persian-friendly stream logger.
- `pformat(template, *args, **kwargs)`: Visual alignment and `:fa`/`:p` format specifier.
- `persian_fstring(template, **kwargs)`: Context-capturing Persian f-string.

---

## 4. Remediation Plan for v3.3.1

1. **Bug Fixes:**
   - Fix f-string syntax in `parsikit/dev.py` for Python 3.10 and 3.11 compatibility.
   - Fix `is_jalali_leap` calculation to match the astronomical calendar and `jalali_to_gregorian`.
   - Fix `format_postal_code` in `parsikit/validators.py` to format as `XXXXX-XXXXX`.
   - Fix `PersianFormatter` in `parsikit/dev.py` to convert `,` to Persian comma `،` when formatting with `fa`/`p`.
   - Add `"نسخه": "neskheh"` to `_COMMON_WORDS_PINGLISH` in `parsikit/text.py`.
   - Convert numeric values in `humanize_relative_time` in `parsikit/datetime.py` to Persian numerals.
   - Clarify `mask_email` docstring and test expectation (1-to-1 character masking).
   - Add `has_persian_digits` detection to `inspect_text`.
2. **Security Hardening:**
   - Add `.masked` property to `BankCard`, `MobileNumber`, and `NationalCode` models.
   - Mask sensitive values in `InvalidCardNumberError` and `InvalidNationalCodeError` exception messages.
   - Ensure safe fallbacks for short inputs in all masking utilities.
3. **Test Reorganization:**
   - Establish `tests/unit/`, `tests/integration/`, `tests/regression/`, `tests/security/`, and `tests/fixtures/`.
   - Add regression tests for all fixed bugs.
   - Provide shared synthetic fixtures (no real PII or bank cards).
4. **Documentation:**
   - Write comprehensive Persian and English documentation covering every public API.
   - Provide runnable examples.
5. **Packaging:**
   - Ensure version consistency across `__init__.py`, `pyproject.toml`, and `setup.py`.
