"""Unit tests for parsikit.reshaper module."""
import unittest
from parsikit.reshaper import reshape_for_graphics, reshape_paragraph_for_graphics


class TestReshaperModule(unittest.TestCase):
    def test_reshape_for_graphics_basic(self):
        # Letters are connected and reshaped
        shaped = reshape_for_graphics("سلام")
        self.assertIsInstance(shaped, str)
        self.assertGreater(len(shaped), 0)
        self.assertEqual(reshape_for_graphics(""), "")

    def test_reshape_with_latin_preservation(self):
        mixed = "Python نسخه 3"
        shaped = reshape_for_graphics(mixed)
        # Latin word 'Python' should be preserved intact
        self.assertIn("Python", shaped)

    def test_reshape_paragraph(self):
        text = "این یک متن طولانی برای آزمایش شکستن خطوط در نرم‌افزارهای گرافیکی است."
        lines = reshape_paragraph_for_graphics(text, max_chars_per_line=25)
        self.assertIsInstance(lines, list)
        self.assertGreater(len(lines), 1)
        self.assertEqual(reshape_paragraph_for_graphics("", 20), [])


if __name__ == "__main__":
    unittest.main()
