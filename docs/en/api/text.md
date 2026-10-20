# Text Processing API (`parsikit.text`)

High-performance, Unicode-aware Persian text standardization, normalization, and keyboard utilities.

---

## Standardization & Normalization

### `standardize_persian(text: str, *, strip_diacritics_opt: bool = False) -> str`
Normalizes raw Persian and mixed-language text according to standard orthographic rules:
- **Unicode Canonical Normalization**: Applies standard Unicode canonical composition (`NFC`), ensuring decomposed sequences (such as decomposed `آ`) match precomposed Persian characters.
- **Arabic Character Mapping**: Converts standard Arabic glyph variants to standard Persian equivalents:
  - Arabic Yeh (`ي` / `\u064A` and `ى` / `\u0649`) → Persian Yeh (`ی` / `\u06CC`)
  - Arabic Kaf (`ك` / `\u0643`) → Persian Keheh (`ک` / `\u06A9`)
  - Arabic Ta Marbuta (`ة` / `\u0629` and `ە` / `\u06D5`) → Persian Heh (`ه` / `\u0647`)
  - Arabic digits (`٠١٢٣٤٥٦٧٨٩`) → Persian digits (`۰۱۲۳۴۵۶۷۸۹`)
- **Zero-Width Non-Joiner (ZWNJ) Engine**:
  - Automatically adjusts half-spaces for standard prefixes (`می‌`, `نمی‌`, `بی‌`) and suffixes (`‌ها`, `‌های`, `‌ترین`, `‌تر`, `‌ای`, etc.).
  - Cleans up space-adjacent ZWNJ pairs (e.g. ` \u200c` or `\u200c ` → `\u200c`).
  - Removes redundant ZWNJs adjacent to punctuation marks.
  - Collapses duplicate consecutive ZWNJs (`\u200C{2,}`) into a single `\u200C`.
  - Trims leading and trailing ZWNJs from text boundaries.
- **Idempotence**: Strictly satisfies `standardize_persian(standardize_persian(x)) == standardize_persian(x)`.
- **Whitespace**: Collapses multiple redundant spaces into a single space and trims edge margins.
- **Optional Diacritics Removal**: When `strip_diacritics_opt=True`, strips vowel diacritics via `strip_diacritics`.

### `strip_diacritics(text: str) -> str`
Removes Persian and Arabic vowel diacritic marks (Fatha, Damma, Kasra, Tanwin, Tashdid, Sukun) via precompiled regular expressions.

### `is_persian(text: str) -> bool`
Returns `True` if the string contains at least one character in the Persian/Arabic Unicode blocks (including Presentation Forms).

### `clean_text(text: str) -> str`
Sanitizes raw or multi-line strings through a comprehensive pipeline:
1. Standardizes characters and ZWNJ via `standardize_persian`.
2. Converts digits to Persian numerals via `english_to_persian`.
3. Beautifies punctuation spacing via `beautify_persian_spacing`.
4. Strips invisible zero-width and bidirectional control characters (`\u200B`, `\uFEFF`, `\u200E-\u200F`, `\u202A-\u202E`), strictly preserving intentional ZWNJ (`\u200C`).
5. Collapses redundant blank lines (allowing at most 1 empty line between paragraphs).
6. Trims leading/trailing spaces per line.

### `normalize_whitespace(text: str, keep_paragraphs: bool = True) -> str`
Normalizes non-standard Unicode spaces (tabs, non-breaking spaces `\u00A0`, thin spaces, narrow spaces) to standard spaces.
- If `keep_paragraphs=True` (default), preserves paragraph separations while clipping redundant blank lines.
- If `keep_paragraphs=False`, flattens all text into a single continuous line.

### `beautify_persian_spacing(text: str) -> str`
Optimizes spacing around Persian and Latin punctuation marks with strict content protection:
- Standardizes Persian commas (`،`) and semicolons (`؛`).
- Removes redundant spaces before punctuation marks (`.`, `،`, `؛`, `؟`, `!`, `:`, `)`).
- Inserts a single space after Persian punctuation (`،`, `؛`, `؟`, `!`).
- **Safety Protection**:
  - **URLs**: Preserves web addresses (e.g. `https://example.com/api`) without inserting spaces after colons or dots.
  - **Emails**: Preserves email addresses (e.g. `kamrani.exe@gmail.com`) without corrupting usernames or domains.
  - **Decimal Numbers**: Preserves floating-point numbers in ASCII and Persian scripts (e.g. `3.14`, `۱۲.۵`).
  - **Timestamps**: Preserves clock times (e.g. `12:30`, `۱۴:۴۵`).
  - **Code & Filenames**: Preserves technical file extensions (e.g. `test.py`, `script.min.js`).
  - **Ellipses**: Preserves consecutive dots (`...`).

---

## Keyboard Layout & Collation

### `correct_keyboard_layout(text: str) -> str`
Translates Persian text accidentally typed while the system keyboard was set to English QWERTY into proper Persian characters (e.g. `"sghl"` → `"سلام"`).

### `persian_sort_key(s: str) -> tuple[int, ...]`
Generates a precomputed sorting key tuple respecting the official Persian alphabet collation order (`آابپتثجچحخدذرزژسشصضطظعغفقکگلمنوهی`), normalizing Arabic variants (`أ`, `إ`, `ٱ`, `ؤ`, `ئ`) into base Persian letters, placing ZWNJ before space, and ordering numbers before letters.

### `persian_sorted(iterable: Iterable[T], *, reverse: bool = False) -> list[T]`
Sorts an iterable of strings using the optimized Persian collation key.

---

## Extraction & Conversion

### `words_to_number(text: str) -> int`
High-performance parser converting Persian textual number expressions (e.g. `"سی و دو هزار و پانصد"`) into exact integers (`32500`). Supports negative numbers (`"منفی پنجاه"` → `-50`), compound scale multipliers (e.g. `"هزار میلیارد"` → `1000000000000`), and large magnitudes up to septillions.

### `convert_numbers(text: str, to: Literal["persian", "english"] = "persian") -> str`
Converts numeric digits within arbitrary text between Persian (`۰-۹`) and English (`0-9`) numeral representations.

### `slugify(text: str, separator: str = "-") -> str`
Generates clean, SEO-optimized URL slugs from Persian text with dictionary-backed transliteration:
- Transliterates common words, prepositions, and technical terms (`پایتون` → `python`, `وردپرس` → `wordpress`, `در` → `dar`, `کتاب` → `ketab`).
- Converts digits to ASCII.
- Filters out special characters and collapses repeated separators.

### `extract_mobiles(text: str) -> list[str]`
Extracts and validates all unique Iranian mobile phone numbers found in unformatted text.

### `extract_national_codes(text: str) -> list[str]`
Extracts and validates all 10-digit Iranian National Codes satisfying the official civil registration checksum.

---

## Sensitive Data Masking

### `mask_mobile(phone: str, mask_char: str = "*") -> str`
Masks the middle digits of an Iranian mobile number (e.g. `"09123456789"` → `"0912***6789"`).

### `mask_card(card: str, mask_char: str = "*") -> str`
Masks the middle digits of a 16-digit debit/credit card number (e.g. `"6037991122334455"` → `"6037-99**-****-4455"`).

### `mask_national_code(code: str, mask_char: str = "*") -> str`
Masks the middle digits of a 10-digit National Code (e.g. `"7730123452"` → `"773-****45-2"`).

### `mask_email(email: str, mask_char: str = "*") -> str`
Masks username characters in an email address (e.g. `"kamrani.exe@gmail.com"` → `"ka********e@gmail.com"`).

