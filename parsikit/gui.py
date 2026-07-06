"""
parsikit.gui
~~~~~~~~~~~~
Cross-platform, GUI-agnostic dynamic typing helpers for Persian interfaces.
Integrates with Tkinter, CustomTkinter, PySide, and PyQt.
"""

from __future__ import annotations
from typing import Literal, Any, Callable
from parsikit.text import standardize_persian, beautify_persian_spacing


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
    _TO_ENGLISH = str.maketrans("۰۱۲۳۴۵۶۷۸۹٠١٢٣٤٥٦٧٨٩", "01234567890123456789")
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


def _format_text(val: str) -> str:
    return beautify_persian_spacing(standardize_persian(val))


_FORMATTERS: dict[str, Callable[[str], str]] = {
    "text": _format_text,
    "national_code": _format_national_code,
    "card_number": _format_card_number,
    "postal_code": _format_postal_code,
    "sheba": _format_sheba,
}


def _bind_tkinter(widget: Any, formatter: Callable[[str], str]) -> None:
    def on_key_release(event: Any) -> None:
        if event.keysym in ("Shift_L", "Shift_R", "Control_L", "Control_R", "Alt_L", "Alt_R", "Caps_Lock", "Num_Lock", "Scroll_Lock"):
            return
            
        cursor_pos = widget.index("insert")
        old_val = widget.get()
        new_val = formatter(old_val)
        
        if old_val != new_val:
            diff = len(new_val) - len(old_val)
            widget.delete(0, "end")
            widget.insert(0, new_val)
            new_pos = max(0, min(len(new_val), cursor_pos + diff))
            widget.icursor(new_pos)
            
    widget.bind("<KeyRelease>", on_key_release)


def _bind_qt(widget: Any, formatter: Callable[[str], str]) -> None:
    def on_text_edited(text: str) -> None:
        widget.textEdited.disconnect(on_text_edited)
        
        cursor_pos = widget.cursorPosition()
        old_len = len(text)
        new_val = formatter(text)
        widget.setText(new_val)
        
        diff = len(new_val) - old_len
        widget.setCursorPosition(max(0, min(len(new_val), cursor_pos + diff)))
        
        widget.textEdited.connect(on_text_edited)
        
    widget.textEdited.connect(on_text_edited)


def bind_persian_input(
    widget: Any, 
    input_type: Literal["text", "national_code", "card_number", "postal_code", "sheba"] = "text"
) -> None:
    """Binds real-time typing assistance and formatting to a GUI widget."""
    if input_type not in _FORMATTERS:
        raise ValueError(f"Unknown input_type '{input_type}'. Supported types: {list(_FORMATTERS.keys())}")
        
    formatter = _FORMATTERS[input_type]
    
    if hasattr(widget, "_entry"):
        target_widget = widget._entry
    else:
        target_widget = widget
        
    if hasattr(target_widget, "bind") and hasattr(target_widget, "insert") and hasattr(target_widget, "delete"):
        _bind_tkinter(target_widget, formatter)
    elif hasattr(target_widget, "textEdited") and hasattr(target_widget, "setText") and hasattr(target_widget, "setCursorPosition"):
        _bind_qt(target_widget, formatter)
    else:
        raise TypeError("Unsupported widget. Must be a Tkinter Entry, CustomTkinter CTkEntry, or PyQt/PySide QLineEdit.")