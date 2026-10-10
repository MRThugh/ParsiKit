# Developer Diagnostics & GUI API (`parsikit.dev`, `parsikit.gui`, `parsikit.reshaper`)

## Visual Alignment & Diagnostics (`parsikit.dev`)

### `pformat(template: str, *args, **kwargs) -> str`
Persian-aware string formatter that accounts for Zero-Width Non-Joiner (ZWNJ) characters and diacritics when calculating visual padding. Supports `:fa` / `:p` format specifiers.

### `persian_fstring(template: str, **kwargs) -> str`
Formatted string evaluation with automatic visual alignment and Persian digit conversion.

### `inspect_text(text: str) -> dict`
Analyzes string structure and reports character counts, ZWNJ count, Arabic characters, and digit scripts.

### `debug_text(text: str) -> None`
Prints a formatted diagnostic report to stdout.

### `validate_batch(items: list, model_class, silent: bool = False) -> dict`
Validates a list of raw inputs against a ParsiKit model class and returns valid/invalid summaries.

---

## Graphical Reshaping & Input Binding (`parsikit.reshaper`, `parsikit.gui`)

### `reshape_for_graphics(text: str, reverse: bool = True) -> str`
Reshapes cursive Persian text and reverses character order for 2D graphics renderers without HarfBuzz support (PIL, OpenCV, Pygame).

### `reshape_paragraph_for_graphics(text: str, max_chars_per_line: int, reverse: bool = True) -> str`
Splits and reshapes multi-line text blocks.

### `bind_persian_input(widget, input_type: str = "text") -> None`
Attaches live keystroke normalization to Tkinter and CustomTkinter input entries.
