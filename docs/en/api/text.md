# Text Processing API (`parsikit.text`)

High-performance, Unicode-aware Persian text standardization, normalization, and keyboard utilities.

---

## Standardization & Normalization

### `standardize_persian(text: str, *, strip_diacritics_opt: bool = False, preserve_arabic: bool = False) -> str`
Normalizes raw Persian and mixed-language text according to standard orthographic rules:
- **Scope & Multilingual Support**:
  - By default (`preserve_arabic=False`), standardizes text within a Persian orthographic context, mapping Arabic loanword variants to standard Persian letters:
    - Arabic Yeh (`ي` / `\u064A` and `ى` / `\u0649`) → Persian Yeh (`ی` / `\u06CC`)
    - Arabic Kaf (`ك` / `\u0643`) → Persian Keheh (`ک` / `\u06A9`)
    - Arabic Ta Marbuta (`ة` / `\u0629`) → Persian Heh (`ه` / `\u0647`) in loanwords (e.g. `دایرة المعارف` → `دایره المعارف`)
    - Arabic digits (`٠١٢٣٤٥٦٧٨٩`) → Persian digits (`۰۱۲۳۴۵۶۷۸۹`)
    - Heh with Yeh Above (`ۀ` / `\u06C0`) → `هٔ` (`\u0647\u0654`)
  - When `preserve_arabic=True`, Arabic-specific characters (`ة`, `ي`, `ى`) are strictly preserved, preventing unwanted alteration of Arabic text (e.g. `"هذه لغة عربية جميلة"`).
  - Kurdish characters such as Kurdish Ae (`ە` / `\u06D5`) are **never** converted to `ه` and remain completely preserved.
  - English and other Latin-script words remain unmodified.
- **Unicode Canonical Normalization**: Applies standard Unicode canonical composition (`NFC`), ensuring decomposed sequences (such as decomposed `آ`) match precomposed Persian characters.
- **Zero-Width Non-Joiner (ZWNJ) Engine**:
  - Automatically adjusts half-spaces for standard prefixes (`می‌`, `نمی‌`, `بی‌`) and suffixes (`‌ها`, `‌های`, `‌ترین`, `‌تر`, `‌ای`, etc.).
  - Preserves word boundaries: spaces surrounding ZWNJ between independent words (e.g. `"الف \u200c ب"`) collapse into a standard space (`"الف ب"`), ensuring separate words are not unintentionally conjoined.
  - Cleans up single-sided space-adjacent ZWNJ (e.g. `"دانش \u200cآموز"` → `"دانش\u200cآموز"`), preserving meaningful Persian half-spaces.
  - Removes redundant ZWNJs adjacent to punctuation marks (`.`, `،`, `؛`, `؟`, `!`, `:`, `()`, `[]`, `{}`, `«»`).
  - Collapses duplicate consecutive ZWNJs (`\u200C{2,}`) into a single `\u200C`.
  - Trims leading and trailing ZWNJs from text boundaries.
- **Idempotence**: Strictly satisfies `standardize_persian(standardize_persian(x)) == standardize_persian(x)`.
- **Whitespace & Line Breaks**: Collapses redundant spaces into a single space and trims edge margins while preserving line breaks and paragraph structure.
- **Optional Diacritics Removal**: When `strip_diacritics_opt=True`, strips vowel diacritics via `strip_diacritics`.

### `strip_diacritics(text: str) -> str`
Removes Persian and Arabic vowel diacritic marks (Fatha, Damma, Kasra, Tanwin, Tashdid, Sukun) via precompiled regular expressions.

### `is_persian(text: str) -> bool`
Returns `True` if the string contains at least one character in the Persian/Arabic Unicode blocks (including Presentation Forms).

### `clean_text(text: str, *, preserve_arabic: bool = False) -> str`
Sanitizes raw or multi-line strings through a comprehensive pipeline:
1. **Token Protection**: Shields URLs, email addresses, key-value configurations, semantic versions, and technical IDs from digit conversions and spacing modifications.
2. **Standardization**: Normalizes characters and ZWNJ layout via `standardize_persian(..., preserve_arabic=preserve_arabic)`.
3. **Digit Conversion**: Converts prose ASCII and Arabic numbers to Persian numerals via `english_to_persian`, while strictly keeping technical identifiers and URLs in ASCII.
4. **Spacing Beautification**: Optimizes punctuation spacing via `beautify_persian_spacing`.
5. **Control Character Stripping**: Strips invisible zero-width and bidirectional control characters (`\u200B`, `\uFEFF`, `\u200E-\u200F`, `\u202A-\u202E`), strictly preserving intentional ZWNJ (`\u200C`).
6. **Paragraph Clean-up**: Collapses redundant blank lines (allowing at most 1 empty line between paragraphs) and trims margins per line.
7. **Token Restoration**: Restores protected URLs, emails, and technical strings to their exact original forms.

### `normalize_whitespace(text: str, keep_paragraphs: bool = True) -> str`
Normalizes non-standard Unicode spaces (tabs, non-breaking spaces `\u00A0`, thin spaces, narrow spaces) to standard spaces.
- If `keep_paragraphs=True` (default), preserves paragraph separations while clipping redundant blank lines.
- If `keep_paragraphs=False`, flattens all text into a single continuous line.

### `beautify_persian_spacing(text: str) -> str`
Optimizes spacing around Persian and Latin punctuation marks with strict content protection:
- Standardizes Persian commas (`،`) and semicolons (`؛`).
- Removes redundant spaces before punctuation marks (`.`, `،`, `؛`, `؟`, `!`, `:`, `)`).
- Inserts a single space after Persian punctuation (`،`, `؛`, `؟`, `!`).
- Adjusts spacing around parentheses, brackets, and Persian quotation marks (`«»`), ensuring closing brackets followed by sentence punctuation (`.`, `،`) do not gain unwanted spaces.
- Does NOT alter digits.
- **Safety Protection**:
  - **URLs**: Preserves web addresses, query strings (`?x=1&y=2`), paths, ports (`:8080`), fragments (`#section`), and percent-encoding (`%20`) without inserting spaces after question marks, colons, or slashes.
  - **Trailing Sentence Punctuation**: Punctuation following a URL or closing parenthesis is formatted cleanly without being absorbed into the URL or separated by redundant spaces.
  - **Emails**: Preserves email addresses (e.g. `user.name+tag@example.co.uk`) without corrupting usernames or domains.
  - **Decimal Numbers**: Preserves floating-point numbers in ASCII and Persian scripts (e.g. `3.14`, `۱۲.۵`).
  - **Timestamps**: Preserves clock times (e.g. `12:30`, `۱۴:۴۵`).
  - **Technical Tokens**: Preserves version strings (e.g. `version=v2.0.1`, `Python 3.13.3`) and technical IDs (e.g. `ID-2026-0042`).
  - **Code & Filenames**: Preserves technical file extensions (e.g. `test.py`, `script.min.js`).
  - **Ellipses**: Preserves consecutive dots (`...`).

### `smart_persian_spacing(text: str, preserve_urls: bool = True, preserve_quotes: bool = True) -> str`
Applies contextual half-space (ZWNJ) normalization and spacing corrections around Persian prefixes (`می‌`, `نمی‌`, `بی‌`), suffixes (`‌ها`, `‌های`, `‌ترین`, `‌تر`, `‌ای`), punctuation marks, and quotation marks, with strict protection for URLs, email addresses, and quoted spans.

---

## Keyboard Layout & Collation

### `correct_keyboard_layout(text: str, to: Literal["persian", "english", "auto"] = "persian", preserve_mixed: bool = False) -> str`
Translates text mistyped under the wrong keyboard layout between Persian and English QWERTY:
- `to="persian"`: Converts English QWERTY keystrokes to Persian (e.g. `"sghl"` → `"سلام"`). Preserves already-correct Persian text.
- `to="english"`: Converts Persian keystrokes to English QWERTY (e.g. `"اثممخ"` → `"hello"`).
- `to="auto"`: Detects script dominance and converts to the opposite layout.
- `preserve_mixed`: When `True`, avoids corrupting mixed alphanumeric codes or identifiers.

### `expand_snippets(text: str, snippets: dict[str, str], word_boundary: bool = True) -> str`
Replaces shorthand abbreviations and snippets with their expanded forms (e.g. `{"ق.ظ": "قبل از ظهر", "ب.ظ": "بعد از ظهر"}`). Uses regex word boundaries when `word_boundary=True`.

### `persian_sort_key(s: str) -> tuple[int, ...]`
Generates a precomputed sorting key tuple respecting the official Persian alphabet collation order (`آابپتثجچحخدذرزژسشصضطظعغفقکگلمنوهی`), normalizing Arabic variants (`أ`, `إ`, `ٱ`, `ؤ`, `ئ`) into base Persian letters, placing ZWNJ before space, and ordering numbers before letters.

### `persian_sorted(iterable: Iterable[T], *, reverse: bool = False) -> list[T]`
Sorts an iterable of strings using the optimized Persian collation key.

---

## Extraction & Conversion

### `normalize_digits(text: str, to: Literal["persian", "english", "arabic"] = "persian") -> str`
Converts all digits across Latin, Persian, and Arabic-Indic Unicode blocks to a single uniform numeral system: `"persian"` (`۰-۹`), `"english"` (`0-9`), or `"arabic"` (`٠-٩`).

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

