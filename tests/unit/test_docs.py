"""
Unit test for ParsiKit 4-language documentation integrity.
Runs the comprehensive automated documentation validation.
"""

import unittest
from scripts.validate_docs import validate


class TestFourLanguageDocumentation(unittest.TestCase):
    def test_documentation_integrity(self):
        """Validate that all 4 documentation editions are complete and error-free."""
        self.assertTrue(validate(), "Documentation integrity check failed!")


if __name__ == "__main__":
    unittest.main()
