# Reshaper API (`parsikit.reshaper`)

Lightweight, zero-dependency Persian letter connection shaper and Bidirectional (BiDi) layout reorganizer for graphic engines, image generation libraries, and games.

---

## Overview

Most graphic engines (such as Pygame, OpenCV, Pillow without `raqm`, Matplotlib, OpenGL, and PDF generators) assume left-to-right Latin typography. When rendering Persian text without a shaping engine, letters appear disconnected, disjointed, and backwards (e.g. `س ل ا م` instead of `سلام`).

`parsikit.reshaper` converts standard Persian Unicode characters into their contextual contextual presentation forms (Isolated, Initial, Medial, Final) and reorders glyphs for naive LTR renderers.

---

## Public Functions

### `reshape_for_graphics(text: str, reverse: bool = True) -> str`

Connects cursive Persian characters into appropriate presentation glyphs and manages bidirectional text blocks.

#### Parameters:
- **`text`** (`str`): The Persian or mixed Persian-Latin string to reshape.
- **`reverse`** (`bool`, default `True`): If `True`, reverses RTL character order for graphics engines that draw from left to right. Embedded Latin words and digits are preserved in correct left-to-right order.

#### Returns:
- `str`: Shaped Unicode presentation string ready for graphic blitting.

#### Direction & Reversal Semantics:
- **`reverse=True` (Default)**: Intended for naive graphic rendering environments (such as basic Pygame, OpenCV, Matplotlib, or simple Canvas) that draw characters strictly from left to right. RTL character runs are inverted so they draw correctly from right to left, while embedded LTR runs (Latin words, URLs, emails, dates, and numbers) remain in forward left-to-right reading order.
- **`reverse=False`**: Intended for engines that already handle BiDi cursor positioning or text flow, but lack font cursive shaping support. Only glyph shaping (Initial, Medial, Final, Isolated) and Lam-Alef ligatures are performed, preserving original logical character order.

#### Supported Features:
- Complete Persian and Arabic alphabet presentation mapping (including `ۀ`, `ك`, `ي`, and Kurdish `ە`).
- Standard **Lam-Alef ligatures** (`لا`, `لآ`, `لأ`, `لإ`) in isolated and final positions.
- **Diacritics & Combining Graphemes**: Ignores short vowels during connectivity checks and preserves combining diacritics attached to base letters upon reversal.
- **BiDi Block & Numeral Preservation**: Preserves Latin words, URLs, emails, dates, and numbers (both ASCII and Persian/Arabic digits) in standard LTR order without inversion.

#### Limitations & Boundary Scope:
`parsikit.reshaper` is a lightweight, zero-dependency layout helper. It is **not** a complete implementation of the Unicode Bidirectional Algorithm (UAX #9). While it correctly segments sequential RTL and LTR blocks (including embedded Latin phrases, numbers, and URLs), deeply nested bidirectional text (e.g., an Arabic clause embedded within an English phrase inside a Persian sentence with complex punctuation neutrals) requires a specialized full-layout engine such as HarfBuzz with Raqm/FriBidi.

#### Usage Example:

```python
import parsikit

raw_text = "سلام دنیا (نسخه 3.3.1)"
# Shaped and reversed for Pygame or Pillow:
ready_text = parsikit.reshape_for_graphics(raw_text)

# Shaped without reversing (for engines with native BiDi but lacking font shaping):
shaped_only = parsikit.reshape_for_graphics(raw_text, reverse=False)
```

---

### `reshape_paragraph_for_graphics(text: str, max_chars_per_line: int, reverse: bool = True) -> list[str]`

Automatically word-wraps a long paragraph of Persian text and reshapes each line for graphical drawing.

#### Parameters:
- **`text`** (`str`): Paragraph text to wrap and shape.
- **`max_chars_per_line`** (`int`): Maximum character width per line.
- **`reverse`** (`bool`, default `True`): Whether to reverse RTL blocks for LTR canvas drawing.

#### Returns:
- `list[str]`: A list of shaped line strings.

#### Usage Example:

```python
import parsikit

paragraph = "پارسی‌کیت یک کتابخانه استاندارد پایتونی برای پردازش اطلاعات فارسی، تقویم شمسی و اعتبارسنجی است."
lines = parsikit.reshape_paragraph_for_graphics(paragraph, max_chars_per_line=30)
for line in lines:
    print(line)
```

---

## Relationship to Other Modules

- **`parsikit.text.standardize_persian`**: Recommended before shaping to unify Arabic characters and fix zero-width non-joiners.
- **`parsikit.gui.bind_persian_input`**: Integrates live typing assistance for GUI frameworks (Tkinter, CustomTkinter, Qt).

