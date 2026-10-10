"""
Security, privacy, and sensitive data protection tests for ParsiKit.
"""
import unittest
import parsikit
from parsikit.exceptions import InvalidCardNumberError, InvalidNationalCodeError
from parsikit.text import mask_card, mask_mobile, mask_national_code, mask_email


class TestSecurityAndPrivacy(unittest.TestCase):
    def test_bank_card_masking_property_and_exception_safety(self):
        card = parsikit.BankCard("6037991122334455")
        self.assertEqual(card.masked, "6037-99**-****-4455")

        # In to_dict()
        d = card.to_dict()
        self.assertIn("masked", d)
        self.assertEqual(d["masked"], "6037-99**-****-4455")

        # Verify that an invalid 16-digit card number is masked in the exception message
        raw_invalid_card = "6037991122334456"
        try:
            parsikit.BankCard(raw_invalid_card)
            self.fail("Expected InvalidCardNumberError was not raised")
        except InvalidCardNumberError as e:
            error_msg = str(e)
            # The full unmasked card number must not appear in the error message
            self.assertNotIn("6037991122334456", error_msg)
            self.assertIn("6037-99**-****-4456", error_msg)

    def test_national_code_masking_property_and_exception_safety(self):
        nc = parsikit.NationalCode("7730123452")
        self.assertEqual(nc.masked, "773-****45-2")

        d = nc.to_dict()
        self.assertIn("masked", d)
        self.assertEqual(d["masked"], "773-****45-2")

        # Verify that an invalid national code is masked in the exception message
        raw_invalid_code = "7730123459"
        try:
            parsikit.NationalCode(raw_invalid_code)
            self.fail("Expected InvalidNationalCodeError was not raised")
        except InvalidNationalCodeError as e:
            error_msg = str(e)
            self.assertNotIn("7730123459", error_msg)
            self.assertIn("773-****45-9", error_msg)

    def test_mobile_number_masking_property(self):
        mob = parsikit.MobileNumber("09123456789")
        self.assertEqual(mob.masked, "0912***6789")

        d = mob.to_dict()
        self.assertIn("masked", d)
        self.assertEqual(d["masked"], "0912***6789")

    def test_masking_edge_and_malformed_inputs(self):
        # Empty inputs must not crash
        self.assertEqual(mask_card(""), "")
        self.assertEqual(mask_mobile(""), "")
        self.assertEqual(mask_national_code(""), "")
        self.assertEqual(mask_email(""), "")

        # Short inputs must not crash or leak out-of-bounds
        self.assertIsInstance(mask_card("123"), str)
        self.assertIsInstance(mask_mobile("09"), str)
        self.assertIsInstance(mask_national_code("123"), str)
        self.assertIsInstance(mask_email("a@b.com"), str)
        self.assertIsInstance(mask_email("plain-text"), str)

    def test_checksum_vs_ownership_guarantees(self):
        """
        Verify that is_valid_* functions perform structural/checksum verification
        and do not imply external identity verification.
        """
        # A syntactically valid national code passes checksum but provides no identity verification
        self.assertTrue(parsikit.is_valid_national_code("7730123452"))
        # A syntactically valid card passes Luhn check but cannot confirm cardholder identity
        self.assertTrue(parsikit.is_valid_card_number("6037991122334455"))


if __name__ == "__main__":
    unittest.main()
