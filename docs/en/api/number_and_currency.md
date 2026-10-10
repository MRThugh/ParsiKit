# Numbers & Currency API (`parsikit.number`, `parsikit.currency`)

## Numbers (`parsikit.number`)

### `english_to_persian(text: str) -> str`
Replaces English digits (`0-9`) with Persian digits (`۰-۹`).

### `persian_to_english(text: str) -> str`
Replaces Persian and Arabic digits with English ASCII digits.

### `number_to_words(number: int | float) -> str`
Translates integers up to 999 septillion into written Persian words.

---

## Currency (`parsikit.currency`)

### `rial_to_toman(amount: int | float) -> int | float`
Converts Rial to Toman by dividing by 10.

### `toman_to_rial(amount: int | float) -> int | float`
Converts Toman to Rial by multiplying by 10.

### `format_currency(amount, currency="toman", *, persian_digits=False) -> str`
Formats a numeric amount with thousand separators and currency symbol.

### `format_currency_to_words(amount, currency="toman") -> str`
Expresses an amount in written Persian words with the currency label.

### `add_tax_and_toll(amount, tax_rate=None) -> dict`
Calculates Value-Added Tax (VAT) and the total price.

### `calculate_installments(principal, annual_interest_rate, months) -> dict`
Calculates loan amortization schedule according to the Central Bank of Iran formula.
