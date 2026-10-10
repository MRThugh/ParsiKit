"""Unit tests for parsikit.gui module."""
import unittest
from parsikit.gui import bind_persian_input, _format_national_code, _format_card_number, _format_postal_code, _format_sheba


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


if __name__ == "__main__":
    unittest.main()
