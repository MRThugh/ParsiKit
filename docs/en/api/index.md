# ParsiKit API Reference (English)

Complete reference for all public modules and functions in **ParsiKit**:

| Module | Description | Documentation |
|---|---|---|
| `parsikit.text` | Character standardization, ZWNJ, diacritics stripping, entity extraction, and masking | [Text Reference](text.md) |
| `parsikit.validators` | National Code, mobile, landline, card, Sheba, bill, and plate validators | [Validators Reference](validators.md) |
| `parsikit.models` | Rich domain models for identity and financial types (with Pydantic support) | [Models Reference](models.md) |
| `parsikit.datetime` | Jalali-Gregorian conversions, leap years, month names, and relative time | [Datetime Reference](datetime.md) |
| `parsikit.number` & `parsikit.currency` | Numeral script conversions, words-to-numbers, Rial/Toman, VAT, installments | [Numbers & Currency](number_and_currency.md) |
| `parsikit.dev` & `parsikit.gui` | Visual width alignment, terminal diagnostics, and live typing helpers | [Dev & GUI Reference](dev_and_gui.md) |
| `parsikit.reshaper` | Persian cursive letter reshaping and Bidirectional reordering for graphics | [Reshaper Reference](reshaper.md) |
| `parsikit.cache` | High-performance thread-safe LRU-like caching infrastructure | [Cache Reference](cache.md) |
| `parsikit.config` & `parsikit.exceptions` | Global configuration and structured exception classes | [Config & Exceptions](#configuration--exceptions) |

---

## Configuration & Exceptions

### Configuration (`parsikit.config`)
- `default_tax_rate: float`: Default VAT rate (default: `0.10`).
- `default_currency: str`: System currency default, `"toman"` or `"rial"` (default: `"toman"`).
- `enable_cache: bool`: Thread-safe LRU caching toggle for number-to-words conversions (default: `True`).

### Exceptions (`parsikit.exceptions`)
All custom exceptions inherit from `ParsiKitError` and `ValidationError` (subclass of `ValueError`):
- `InvalidNationalCodeError`
- `InvalidMobileError`
- `InvalidCardNumberError`
- `InvalidShebaError`
- `InvalidPostalCodeError`
- `InvalidPlateError`
- `InvalidBillError`
