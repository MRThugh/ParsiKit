# Developer Diagnostics & GUI API (`parsikit.dev`, `parsikit.gui`, `parsikit.reshaper`)

## Visual Alignment & Diagnostics (`parsikit.dev`)

### `pformat(template: str, *args, **kwargs) -> str`
Persian-aware string formatter that accounts for Zero-Width Non-Joiner (ZWNJ) characters and diacritics when calculating visual padding. Supports `:fa` / `:p` format specifiers.

### `persian_fstring(template: str, **kwargs) -> str`
Formatted string evaluation with automatic visual alignment and Persian digit conversion.

### `inspect_text(text: str) -> dict`
Analyzes string structure and reports character counts, ZWNJ count, Arabic characters, and digit scripts.

### `debug_text(text: str) -> None`
Prints a formatted diagnostic report to stdout. Terminal color output adheres to standards: respects `NO_COLOR`, `FORCE_COLOR`, Windows Terminal (`WT_SESSION`), ConEmu, and modern Windows console ANSI mode.

### `validate_batch(items: list, model_class, silent: bool = False) -> dict`
Validates a list of raw inputs against a ParsiKit model class and returns valid/invalid summaries.

---

## Graphical Reshaping & Input Binding (`parsikit.reshaper`, `parsikit.gui`)

### `reshape_for_graphics(text: str, reverse: bool = True) -> str`
Reshapes cursive Persian text and reverses character order for 2D graphics renderers without HarfBuzz support (PIL, OpenCV, Pygame).

### `reshape_paragraph_for_graphics(text: str, max_chars_per_line: int, reverse: bool = True) -> str`
Splits and reshapes multi-line text blocks.

### `bind_persian_input(widget, input_type: str = "text", *, digit_style: str = "auto", smart_spacing: bool = False, snippets: dict[str, str] | None = None, enable_shortcuts: bool = True) -> None`
Attaches live keystroke normalization, automated Persian keyboard mapping, and smart formatting to input widgets across desktop toolkits:
- **Supported Toolkits**:
  - Tkinter: `tk.Entry`, `tk.Text`
  - CustomTkinter: `ctk.CTkEntry`
  - Qt: `QLineEdit`, `QTextEdit`, `QPlainTextEdit` across PyQt5, PyQt6, PySide2, and PySide6
- **Smart Cursor Preservation**:
  - Uses content-based relative cursor tracking (`_compute_text_cursor_pos` and `_compute_structured_cursor_pos`).
  - Eliminates cursor jumping when inserting, editing, or deleting characters in the middle or end of text.
- **Parameters**:
  - `input_type`: `"text"`, `"national_code"`, `"mobile"`, `"card"`, or `"sheba"`.
  - `digit_style`: Digit conversion mode: `"auto"` (matches input type), `"persian"`, `"english"`, or `"none"`.
  - `smart_spacing`: If `True`, automatically formats half-spaces (ZWNJ) around prefixes (`می‌`) and suffixes (`‌ها`).
  - `snippets`: Optional dictionary mapping abbreviations to expanded text (e.g. `{"ق.ظ": "قبل از ظهر"}`).
  - `enable_shortcuts`: If `True`, enables desktop shortcuts such as Shift+Space for half-space (ZWNJ) entry in Tkinter.

### `unbind_persian_input(widget) -> None`
Safely detaches Persian input handlers, traces, signal connections, and keyboard event bindings from the specified widget.
