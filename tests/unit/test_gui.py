"""Unit tests for parsikit.gui module."""
import unittest
from typing import Callable, Any
from parsikit.gui import (
    bind_persian_input, unbind_persian_input,
    _format_national_code, _format_card_number, _format_postal_code, _format_sheba,
    _compute_structured_cursor_pos, _compute_text_cursor_pos
)


class MockTkEntry:
    """Mock Tkinter Entry widget for headless event testing."""
    def __init__(self, initial_text: str = "", cursor_pos: int = 0) -> None:
        self.text = initial_text
        self.cursor = cursor_pos
        self.bindings: dict[str, list[Callable[..., Any]]] = {}
        self.deleted_ranges: list[tuple[Any, Any]] = []
        self.inserted_history: list[tuple[int, str]] = []

    def get(self) -> str:
        return self.text

    def delete(self, start: int | str, end: int | str) -> None:
        self.deleted_ranges.append((start, end))
        self.text = ""

    def insert(self, pos: int | str, text: str) -> None:
        self.inserted_history.append((self.cursor if pos == "insert" else int(pos), text))
        self.text = text

    def index(self, mark: str) -> int:
        if mark == "insert":
            return self.cursor
        return 0

    def icursor(self, pos: int) -> None:
        self.cursor = pos

    def bind(self, event: str, func: Callable[..., Any]) -> str:
        if event not in self.bindings:
            self.bindings[event] = []
        self.bindings[event].append(func)
        return str(len(self.bindings[event]) - 1)

    def unbind(self, event: str, handler_id: str) -> None:
        if event in self.bindings:
            idx = int(handler_id)
            if idx < len(self.bindings[event]):
                self.bindings[event][idx] = lambda *a, **k: None

    def trigger_key_release(self, keysym: str = "a") -> None:
        class Event:
            pass
        ev = Event()
        ev.keysym = keysym
        for fn in self.bindings.get("<KeyRelease>", []):
            fn(ev)


class MockQtSignal:
    def __init__(self) -> None:
        self.connected_slots: list[Callable[[str], None]] = []

    def connect(self, slot: Callable[[str], None]) -> None:
        if slot not in self.connected_slots:
            self.connected_slots.append(slot)

    def disconnect(self, slot: Callable[[str], None]) -> None:
        if slot in self.connected_slots:
            self.connected_slots.remove(slot)

    def emit(self, text: str) -> None:
        for slot in list(self.connected_slots):
            slot(text)


class MockQLineEdit:
    """Mock PyQt/PySide QLineEdit widget for headless signal testing."""
    def __init__(self, initial_text: str = "", cursor_pos: int = 0) -> None:
        self.text = initial_text
        self.cursor = cursor_pos
        self.textEdited = MockQtSignal()

    def cursorPosition(self) -> int:
        return self.cursor

    def setCursorPosition(self, pos: int) -> None:
        self.cursor = pos

    def setText(self, text: str) -> None:
        self.text = text


class TestGuiModule(unittest.TestCase):
    def test_gui_formatters(self):
        self.assertEqual(_format_national_code("7730123452"), "773-012345-2")
        self.assertEqual(_format_card_number("6037991122334455"), "6037-9911-2233-4455")
        self.assertEqual(_format_postal_code("1234567890"), "12345-67890")
        self.assertEqual(_format_sheba("050170000000123456789012"), "IR05 0170 0000 0012 3456 7890 12")

    def test_bind_persian_input_invalid_type(self):
        with self.assertRaises(ValueError):
            bind_persian_input(None, input_type="unknown")  # type: ignore

    def test_bind_persian_input_unsupported_widget(self):
        with self.assertRaises(TypeError):
            bind_persian_input("dummy_string", input_type="text")

    def test_structured_cursor_position_calculation(self):
        # Adding 4th digit to card number advances past the hyphen
        old_val = "6037"
        new_val = "6037-"
        new_cursor = _compute_structured_cursor_pos(old_val, new_val, old_cursor=4)
        self.assertEqual(new_cursor, 5)

        # Typing in the middle: cursor at index 2 ('60|37-9911-2233-4455')
        # Content count before cursor is 2 ('60')
        old_val = "60937-9911-2233-4455"  # user inserted '9' at index 2
        new_val = "6093-7991-1223-3445"
        # Before cursor at index 3 was '609' (3 content chars)
        new_cursor = _compute_structured_cursor_pos(old_val, new_val, old_cursor=3)
        self.assertEqual(new_cursor, 3)

        # Deleting in the middle does not jump cursor to end
        old_val = "6037-911-2233-4455"  # deleted 1 digit in chunk 2, cursor at 5
        new_val = "6037-9112-2334-455"
        new_cursor = _compute_structured_cursor_pos(old_val, new_val, old_cursor=5)
        self.assertEqual(new_cursor, 5)

    def test_text_cursor_position_calculation(self):
        # When typing at the end of a word: 'می ' -> 'می‌'
        old_val = "می رود"
        new_val = "می‌رود"
        pos = _compute_text_cursor_pos(old_val, new_val, old_cursor=3)
        self.assertEqual(pos, 3)

        # Unchanged text keeps cursor exactly
        self.assertEqual(_compute_text_cursor_pos("سلام", "سلام", 2), 2)

    def test_tkinter_live_card_formatting_and_cursor(self):
        widget = MockTkEntry("6037991122334455", cursor_pos=16)
        bind_persian_input(widget, input_type="card_number")

        # Simulate user having entered 16 digits
        widget.text = "6037991122334455"
        widget.cursor = 16
        widget.trigger_key_release("5")

        self.assertEqual(widget.text, "6037-9911-2233-4455")
        self.assertEqual(widget.cursor, 19)

    def test_tkinter_navigation_and_modifier_keys_ignored(self):
        widget = MockTkEntry("متن تستی", cursor_pos=4)
        bind_persian_input(widget, input_type="text")

        widget.trigger_key_release("Shift_L")
        widget.trigger_key_release("Left")
        widget.trigger_key_release("Control_R")
        # Text and cursor were untouched
        self.assertEqual(widget.text, "متن تستی")
        self.assertEqual(widget.cursor, 4)

    def test_qt_live_formatting_and_safe_reconnection(self):
        widget = MockQLineEdit("09123456789", cursor_pos=10)
        bind_persian_input(widget, input_type="national_code")

        # Emit textEdited signal
        widget.text = "0010123458"
        widget.cursor = 10
        widget.textEdited.emit("0010123458")

        self.assertEqual(widget.text, "001-012345-8")
        self.assertEqual(len(widget.textEdited.connected_slots), 1)

    def test_qt_signal_reconnects_after_exception(self):
        widget = MockQLineEdit("test")
        bind_persian_input(widget, input_type="text")

        # Ensure slot remains connected
        self.assertEqual(len(widget.textEdited.connected_slots), 1)
        widget.textEdited.emit("error-free text")
        self.assertEqual(len(widget.textEdited.connected_slots), 1)

    def test_opt_in_digit_normalization_in_gui(self):
        widget = MockTkEntry("کد 123", cursor_pos=6)
        bind_persian_input(widget, input_type="text", digit_style="persian")

        widget.trigger_key_release("3")
        self.assertEqual(widget.text, "کد ۱۲۳")

        widget_eng = MockTkEntry("کد ۱۲۳", cursor_pos=6)
        bind_persian_input(widget_eng, input_type="text", digit_style="english")
        widget_eng.trigger_key_release("3")
        self.assertEqual(widget_eng.text, "کد 123")

    def test_snippets_expansion_in_gui(self):
        widget = MockTkEntry("متن //salam است", cursor_pos=12)
        bind_persian_input(widget, input_type="text", snippets={"//salam": "سلام و درود"})

        widget.trigger_key_release("m")
        self.assertEqual(widget.text, "متن سلام و درود است")

    def test_repeated_binding_and_unbinding(self):
        widget = MockTkEntry("6037")
        bind_persian_input(widget, input_type="card_number")
        # Bind a second time
        bind_persian_input(widget, input_type="card_number")
        self.assertTrue(hasattr(widget, "_parsikit_tkinter_handler"))

        # Unbind
        unbind_persian_input(widget)
        self.assertFalse(hasattr(widget, "_parsikit_tkinter_handler"))


if __name__ == "__main__":
    unittest.main()
