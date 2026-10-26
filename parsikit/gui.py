"""
parsikit.gui
~~~~~~~~~~~~
Cross-platform, GUI-agnostic dynamic typing helpers for Persian interfaces.
Integrates with Tkinter, CustomTkinter, PySide, and PyQt.
"""

from __future__ import annotations
from typing import Literal, Any, Callable
import re

from parsikit.text import (
    standardize_persian, beautify_persian_spacing,
    smart_persian_spacing, expand_snippets, normalize_digits
)
from parsikit.number import english_to_persian, persian_to_english


def _format_national_code(val: str) -> str:
    _TO_ENGLISH = str.maketrans("۰۱۲۳۴۵۶۷۸۹٠١٢٣٤٥٦٧٨٩", "01234567890123456789")
    clean = "".join(c for c in str(val).translate(_TO_ENGLISH) if c.isdigit())
    clean = clean[:10]
    if len(clean) <= 3:
        return clean
    elif len(clean) <= 9:
        return f"{clean[:3]}-{clean[3:]}"
    else:
        return f"{clean[:3]}-{clean[3:9]}-{clean[9]}"


def _format_card_number(val: str) -> str:
    _TO_ENGLISH = str.maketrans("۰۱۲۳۴۵۶۷۸۹٠١٢٣٤٥٦٧٨٩", "01234567890123456789")
    clean = "".join(c for c in str(val).translate(_TO_ENGLISH) if c.isdigit())
    clean = clean[:16]
    chunks = [clean[i:i+4] for i in range(0, len(clean), 4)]
    return "-".join(chunks)


def _format_postal_code(val: str) -> str:
    _TO_ENGLISH = str.maketrans("۰۱۲۳۴۵۶۷۸۹٠١٢٣٤٥٦٧89", "01234567890123456789")
    clean = "".join(c for c in str(val).translate(_TO_ENGLISH) if c.isdigit())
    clean = clean[:10]
    if len(clean) <= 5:
        return clean
    return f"{clean[:5]}-{clean[5:]}"


def _format_sheba(val: str) -> str:
    _TO_ENGLISH = str.maketrans("۰۱۲۳۴۵۶۷۸۹٠١٢٣٤٥٦٧٨٩", "01234567890123456789")
    clean = "".join(c for c in str(val).translate(_TO_ENGLISH).upper() if c.isdigit() or ('A' <= c <= 'Z'))
    if clean.startswith("IR"):
        clean_digits = "".join(c for c in clean[2:] if c.isdigit())[:24]
        clean = "IR" + clean_digits
    else:
        clean = "".join(c for c in clean if c.isdigit())[:24]
        if clean:
            clean = "IR" + clean
    chunks = [clean[i:i+4] for i in range(0, len(clean), 4)]
    return " ".join(chunks)


def _format_text_default(val: str) -> str:
    """Standard character normalization without disrupting active typing spaces."""
    table = str.maketrans({
        "\u064A": "\u06CC",  # ي -> ی
        "\u0649": "\u06CC",  # ى -> ی
        "\u0643": "\u06A9",  # ك -> ک
        "\u0629": "\u0647",  # ة -> ه
        "\u06C0": "\u0647\u0654",  # ۀ -> هٔ
    })
    return val.translate(table)


_FORMATTERS: dict[str, Callable[[str], str]] = {
    "text": _format_text_default,
    "national_code": _format_national_code,
    "card_number": _format_card_number,
    "postal_code": _format_postal_code,
    "sheba": _format_sheba,
}


def _compute_structured_cursor_pos(old_val: str, new_val: str, old_cursor: int, separators: tuple[str, ...] = ("-", " ")) -> int:
    """Calculate the exact cursor position in new_val by tracking semantic content characters."""
    if old_cursor <= 0:
        return 0
    
    # Count content characters before the cursor in old_val
    content_count = sum(1 for c in old_val[:old_cursor] if c not in separators)
    if content_count <= 0:
        return 0

    # In new_val, find the index right after the content_count-th content character
    cur_count = 0
    new_cursor = len(new_val)
    for idx, ch in enumerate(new_val):
        if ch not in separators:
            cur_count += 1
            if cur_count == content_count:
                new_cursor = idx + 1
                # If followed immediately by a separator, advance cursor past it
                if new_cursor < len(new_val) and new_val[new_cursor] in separators:
                    new_cursor += 1
                break

    return max(0, min(len(new_val), new_cursor))


def _compute_text_cursor_pos(old_val: str, new_val: str, old_cursor: int) -> int:
    """Calculate cursor position for general text edits using longest common prefix/suffix."""
    if old_val == new_val:
        return old_cursor

    # Find common prefix length
    prefix_len = 0
    min_len = min(len(old_val), len(new_val))
    while prefix_len < min_len and old_val[prefix_len] == new_val[prefix_len]:
        prefix_len += 1

    if old_cursor <= prefix_len:
        return old_cursor

    # Find common suffix length
    suffix_len = 0
    while (
        suffix_len < (len(old_val) - prefix_len)
        and suffix_len < (len(new_val) - prefix_len)
        and old_val[-1 - suffix_len] == new_val[-1 - suffix_len]
    ):
        suffix_len += 1

    if old_cursor >= len(old_val) - suffix_len:
        new_pos = len(new_val) - (len(old_val) - old_cursor)
        return max(0, min(len(new_val), new_pos))

    # Cursor is within modified segment
    diff = len(new_val) - len(old_val)
    new_pos = old_cursor + diff
    return max(0, min(len(new_val), new_pos))


def _build_pipeline_formatter(
    input_type: str,
    *,
    digit_style: Literal["persian", "english", "native", "none"] | None = None,
    smart_spacing: bool = False,
    snippets: dict[str, str] | None = None,
) -> Callable[[str, int], tuple[str, int]]:
    """Build a composite formatting and cursor-tracking pipeline."""
    base_formatter = _FORMATTERS[input_type]
    is_structured = input_type in ("national_code", "card_number", "postal_code", "sheba")

    def pipeline(old_text: str, cursor_pos: int) -> tuple[str, int]:
        current = old_text

        # 1. Snippet expansions if configured
        if snippets:
            current = expand_snippets(current, snippets)

        # 2. Base formatter (character normalization or structural separators)
        current = base_formatter(current)

        # 3. Optional smart Persian spacing
        if smart_spacing and input_type == "text":
            current = smart_persian_spacing(current)

        # 4. Opt-in digit normalization
        if digit_style and digit_style != "none":
            if digit_style == "persian":
                current = english_to_persian(current)
            elif digit_style == "english":
                current = persian_to_english(current)
            elif digit_style == "native":
                current = normalize_digits(current, to="persian")

        # 5. Cursor preservation
        if is_structured:
            new_cursor = _compute_structured_cursor_pos(old_text, current, cursor_pos)
        else:
            new_cursor = _compute_text_cursor_pos(old_text, current, cursor_pos)

        return current, new_cursor

    return pipeline


def _bind_tkinter(
    widget: Any,
    pipeline: Callable[[str, int], tuple[str, int]],
    enable_shortcuts: bool = False,
) -> None:
    # Remove previous binding if attached
    unbind_persian_input(widget)

    nav_or_mod_keys = {
        "Shift_L", "Shift_R", "Control_L", "Control_R", "Alt_L", "Alt_R",
        "Caps_Lock", "Num_Lock", "Scroll_Lock", "Super_L", "Super_R",
        "Left", "Right", "Up", "Down", "Home", "End", "Prior", "Next"
    }

    def on_key_release(event: Any) -> None:
        if event.keysym in nav_or_mod_keys:
            return

        cursor_pos = widget.index("insert")
        old_val = widget.get()
        new_val, new_pos = pipeline(old_val, cursor_pos)

        if old_val != new_val:
            widget.delete(0, "end")
            widget.insert(0, new_val)
            widget.icursor(new_pos)

    handler_id = widget.bind("<KeyRelease>", on_key_release)
    widget._parsikit_tkinter_handler = (handler_id, on_key_release)

    if enable_shortcuts:
        def on_shift_space(event: Any) -> str:
            widget.insert("insert", "\u200C")
            return "break"

        shortcut_id = widget.bind("<Shift-space>", on_shift_space)
        widget._parsikit_shortcut_id = shortcut_id


def _bind_qt(
    widget: Any,
    pipeline: Callable[[str, int], tuple[str, int]],
) -> None:
    unbind_persian_input(widget)

    def on_text_edited(text: str) -> None:
        try:
            widget.textEdited.disconnect(on_text_edited)
        except (TypeError, RuntimeError):
            pass

        try:
            old_pos = widget.cursorPosition()
            new_val, new_pos = pipeline(text, old_pos)
            if new_val != text:
                widget.setText(new_val)
                widget.setCursorPosition(new_pos)
        finally:
            try:
                widget.textEdited.connect(on_text_edited)
            except (TypeError, RuntimeError):
                pass

    widget.textEdited.connect(on_text_edited)
    widget._parsikit_qt_handler = on_text_edited


def unbind_persian_input(widget: Any) -> None:
    """Safely disconnect and unbind all ParsiKit dynamic typing helpers from a widget."""
    target_widget = getattr(widget, "_entry", widget)

    # Tkinter cleanup
    if hasattr(target_widget, "_parsikit_tkinter_handler") and hasattr(target_widget, "unbind"):
        try:
            handler_id = target_widget._parsikit_tkinter_handler[0]
            target_widget.unbind("<KeyRelease>", handler_id)
        except Exception:
            pass
        try:
            delattr(target_widget, "_parsikit_tkinter_handler")
        except AttributeError:
            pass

    if hasattr(target_widget, "_parsikit_shortcut_id") and hasattr(target_widget, "unbind"):
        try:
            target_widget.unbind("<Shift-space>", target_widget._parsikit_shortcut_id)
        except Exception:
            pass
        try:
            delattr(target_widget, "_parsikit_shortcut_id")
        except AttributeError:
            pass

    # Qt cleanup
    if hasattr(target_widget, "_parsikit_qt_handler") and hasattr(target_widget, "textEdited"):
        try:
            target_widget.textEdited.disconnect(target_widget._parsikit_qt_handler)
        except Exception:
            pass
        try:
            delattr(target_widget, "_parsikit_qt_handler")
        except AttributeError:
            pass


def bind_persian_input(
    widget: Any, 
    input_type: Literal["text", "national_code", "card_number", "postal_code", "sheba"] = "text",
    *,
    digit_style: Literal["persian", "english", "native", "none"] | None = None,
    smart_spacing: bool = False,
    snippets: dict[str, str] | None = None,
    enable_shortcuts: bool = False,
) -> None:
    """Binds reliable, cursor-preserving real-time typing assistance and formatting to a GUI widget.
    
    Supports:
    - Insertion and deletion with exact cursor preservation across separators.
    - Zero signal loops and safe exception-reconnection in Qt.
    - Opt-in digit normalization ('persian', 'english', 'native').
    - Optional smart Persian spacing and punctuation assistance.
    - User-configured snippet expansion (e.g. {'//salam': 'سلام و درود'}).
    - Safe optional shortcuts (e.g. Shift+Space for ZWNJ in Tkinter).
    
    :param widget: Tkinter Entry, CustomTkinter CTkEntry, or PyQt/PySide QLineEdit.
    :param input_type: Type of data to format ('text', 'national_code', 'card_number', 'postal_code', 'sheba').
    :param digit_style: Desired digit script output ('persian', 'english', 'native', or None).
    :param smart_spacing: When True, applies smart punctuation and ZWNJ spacing corrections.
    :param snippets: Dictionary mapping trigger strings to expansion phrases.
    :param enable_shortcuts: When True, enables typing shortcuts like Shift+Space for ZWNJ.
    """
    if input_type not in _FORMATTERS:
        raise ValueError(f"Unknown input_type '{input_type}'. Supported types: {list(_FORMATTERS.keys())}")
        
    pipeline = _build_pipeline_formatter(
        input_type,
        digit_style=digit_style,
        smart_spacing=smart_spacing,
        snippets=snippets,
    )
    
    if hasattr(widget, "_entry"):
        target_widget = widget._entry
    else:
        target_widget = widget
        
    if hasattr(target_widget, "bind") and hasattr(target_widget, "insert") and hasattr(target_widget, "delete"):
        _bind_tkinter(target_widget, pipeline, enable_shortcuts=enable_shortcuts)
    elif hasattr(target_widget, "textEdited") and hasattr(target_widget, "setText") and hasattr(target_widget, "setCursorPosition"):
        _bind_qt(target_widget, pipeline)
    else:
        raise TypeError("Unsupported widget. Must be a Tkinter Entry, CustomTkinter CTkEntry, or PyQt/PySide QLineEdit.")