"""Integration tests verifying batch validation across various models."""
import unittest
import parsikit


class TestBatchValidationIntegration(unittest.TestCase):
    def test_batch_validation_national_codes(self):
        items = [
            "7730123452",    # Valid
            "1111111111",    # Invalid (repetitive)
            "0010123458",    # Valid (Tehran)
            "invalid-code",  # Invalid format
        ]
        report = parsikit.validate_batch(items, parsikit.NationalCode, silent=True)
        self.assertEqual(report["total"], 4)
        self.assertEqual(report["valid_count"], 2)
        self.assertEqual(report["invalid_count"], 2)
        self.assertEqual(len(report["valid_items"]), 2)
        self.assertEqual(len(report["errors"]), 2)

    def test_batch_validation_mobiles(self):
        items = [
            "09123456789",
            "+989351234567",
            "0912abc",
            "12345",
        ]
        report = parsikit.validate_batch(items, parsikit.MobileNumber, silent=True)
        self.assertEqual(report["total"], 4)
        self.assertEqual(report["valid_count"], 2)
        self.assertEqual(report["invalid_count"], 2)


if __name__ == "__main__":
    unittest.main()
