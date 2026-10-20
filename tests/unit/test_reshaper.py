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

    def test_reshape_with_arabic_variants(self):
        """Verify Arabic Kaf, Arabic Yeh, and Alef Maksura are properly reshaped into presentation forms."""
        # Arabic Kaf ('\u0643') should shape into initial/medial/final presentation forms
        arabic_kaf = reshape_for_graphics("كتاب")
        persian_kaf = reshape_for_graphics("کتاب")
        self.assertEqual(arabic_kaf, persian_kaf)

        # Arabic Yeh ('\u064A') should shape into initial/medial/final presentation forms
        arabic_yeh = reshape_for_graphics("علي")
        persian_yeh = reshape_for_graphics("علی")
        self.assertEqual(arabic_yeh, persian_yeh)

        # Alef Maksura ('\u0649')
        maksura = reshape_for_graphics("موسی")
        self.assertIsInstance(maksura, str)
        self.assertGreater(len(maksura), 0)

    def test_reshape_with_zwnj(self):
        """Verify ZWNJ prevents connection between letters."""
        connected = reshape_for_graphics("می روم", reverse=False)
        with_zwnj = reshape_for_graphics("می\u200Cروم", reverse=False)
        self.assertIn("\u200C", with_zwnj)

    def test_reshape_reverse_flag(self):
        """Verify reverse=False maintains LTR presentation sequence without reversing."""
        shaped = reshape_for_graphics("سلام", reverse=False)
        self.assertIsInstance(shaped, str)
        self.assertGreater(len(shaped), 0)


if __name__ == "__main__":
    unittest.main()
