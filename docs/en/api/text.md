# Text Processing API (`parsikit.text`)

## Functions

### `standardize_persian(text: str, *, strip_diacritics_opt: bool = False) -> str`
Standardizes Persian text by replacing Arabic Yeh and Keheh glyphs, inserting appropriate ZWNJ characters for prefixes (`می‌`, `نمی‌`) and suffixes (`‌ها`, `‌ترین`), and collapsing redundant spaces.

### `strip_diacritics(text: str) -> str`
Removes Persian and Arabic vowel diacritic marks (Fatha, Damma, Kasra, Tanwin, Tashdid, Sukun).

### `is_persian(text: str) -> bool`
Returns `True` if the string contains any Persian/Arabic alphabetic characters.

### `clean_text(text: str) -> str`
Sanitizes multi-line strings by eliminating invisible control characters, standardizing newlines, and cleaning whitespace.

### `normalize_whitespace(text: str, keep_paragraphs: bool = True) -> str`
Collapses whitespace while optionally preserving paragraph structures.

### `correct_keyboard_layout(text: str) -> str`
Translates Persian text accidentally typed on a QWERTY English keyboard layout into proper Persian characters.

### `persian_sort_key(s: str) -> tuple`
Sorting key respecting the official Persian collation order (`گ`, `چ`, `پ`, `ژ`).

### `persian_sorted(iterable, *, reverse: bool = False) -> list`
Sorts an iterable of strings using the Persian collation key.

### `words_to_number(text: str) -> int`
Parses Persian number words into an integer (e.g. `"دویست و پنجاه"` -> `250`).

### `slugify(text: str, separator: str = "-") -> str`
Generates SEO-friendly Finglish URL slugs from Persian text with dictionary-backed transliteration.

### `mask_mobile(phone: str, mask_char: str = "*") -> str`
Masks the middle digits of a mobile phone number (e.g. `"0912***6789"`).

### `mask_card(card: str, mask_char: str = "*") -> str`
Masks the middle 8 digits of a 16-digit debit/credit card number (e.g. `"6037-99**-****-4455"`).

### `mask_national_code(code: str, mask_char: str = "*") -> str`
Masks the middle 4 digits of a 10-digit national code (e.g. `"773-****45-2"`).

### `mask_email(email: str, mask_char: str = "*") -> str`
Masks the middle characters of an email address username (e.g. `"al***i@example.com"`).
