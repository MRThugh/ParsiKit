# ParsiKit Architecture & Technical Design

**Project Owner:** Ali Kamrani (MRThugh)  
**Version:** 3.3.1  
**Target Platform:** Pure Python >= 3.10  

---

## 1. Architectural Philosophy

ParsiKit is built as a **zero-dependency, lightweight, high-performance infrastructure library** for Persian language computing and Iranian domestic data structures.

Core architectural principles:
1. **Zero External Runtime Dependencies:** Standard Python library only (`re`, `datetime`, `math`, `typing`, `logging`, `string`, `ipaddress`). Optional integrations (GUI widgets, Pydantic) use duck-typing and dynamic inspection.
2. **Layered Separation of Concerns:** Pure transformation algorithms live in functional modules (`text`, `number`, `datetime`, `validators`), while rich object-oriented wrappers live in `models`.
3. **Thread-Safe In-Memory Caching:** Computationally intensive astronomical date calculations and written number generation are cached using thread-safe LRU primitives (`parsikit.cache`).
4. **Defensive Validation & Safe Masking:** Differentiate strictly between checksum/syntax validation and authoritative identity verification.

---

## 2. Package Layering

```text
┌────────────────────────────────────────────────────────┐
│             Developer Tools & UI Helpers               │
│         (parsikit.dev, parsikit.gui, parsikit.config)  │
├────────────────────────────────────────────────────────┤
│             Object-Oriented Domain Models              │
│                  (parsikit.models)                     │
├────────────────────────────────────────────────────────┤
│           Domain Algorithms & Formatters               │
│ (parsikit.text, parsikit.validators, parsikit.currency │
│          parsikit.datetime, parsikit.reshaper)         │
├────────────────────────────────────────────────────────┤
│               Low-Level Infrastructure                 │
│         (parsikit.cache, parsikit.exceptions)          │
└────────────────────────────────────────────────────────┘
```

### Module Responsibilities

| Module | Primary Responsibility |
|---|---|
| `parsikit.text` | Text normalization, Arabic-to-Persian character mapping, typography, ZWNJ fixing, sensitive data masking, Pinglish slugification. |
| `parsikit.number` | Digit script translation (Latin <-> Persian <-> Arabic) and written number words up to 999 septillion. |
| `parsikit.currency` | Rial/Toman conversions, currency formatting, VAT calculations, and loan installment amortization. |
| `parsikit.datetime` | Gregorian <-> Jalali astronomical conversions, leap year calculations, relative time humanization. |
| `parsikit.validators` | Checksum verification for National Codes, Card Numbers (Luhn), Sheba (IBAN Modulo-97), Plates, Postal Codes, and Bills. |
| `parsikit.models` | OOP wrappers (`PersianText`, `NationalCode`, `MobileNumber`, `BankCard`, `Sheba`, `VehiclePlate`, `FixedLine`) with duck-typing. |
| `parsikit.reshaper` | Unicode presentation forms shaper and BiDi text reversal for graphics engines without RTL support. |
| `parsikit.gui` | Widget event binder for real-time input formatting in Tkinter and PyQt/PySide. |
| `parsikit.dev` | Development tools: `inspect_text`, `debug_text`, `persian_repr`, `pformat`, `persian_fstring`, `validate_batch`. |
| `parsikit.cache` | Thread-safe in-memory LRU cache decorator. |
| `parsikit.config` | Global configuration options (`default_tax_rate`, `default_currency`, `enable_cache`). |
| `parsikit.exceptions` | Hierarchy of domain exceptions inheriting from `ValidationError` and `ParsiKitError`. |

---

## 3. Backward Compatibility Contract

- **Public Exports:** All symbols exported in `parsikit/__init__.__all__` are guaranteed stable across patch releases.
- **Duck-Typing:** Domain models inherit from `StringLikeMixin` and behave seamlessly as Python strings in equality, length, slicing, and dictionary keys.
- **Pydantic Compatibility:** Models include `PydanticValidationMixin` to enable automatic coercion in Pydantic schemas without hard dependencies.
