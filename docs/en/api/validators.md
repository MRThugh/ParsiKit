# Validators API (`parsikit.validators`)

## Functions

### `is_valid_national_code(code: str, strict: bool = True) -> bool`
Validates a 10-digit Iranian National Code using the official modulo-11 checksum formula. Rejects sequences of 10 identical digits when `strict=True`.

### `format_national_code(code: str) -> str`
Formats a national code in the standard 3-6-1 format (`XXX-XXXXXX-X`).

### `detect_national_code_location(code: str) -> dict | None`
Detects the issuing province and city based on the first three digits of the national code.

### `is_valid_mobile(phone: str) -> bool`
Validates an Iranian mobile phone number across all licensed operators.

### `normalize_mobile(phone: str, prefix: str = "0") -> str`
Normalizes mobile numbers into standard national format (`09...`) or international format (`+989...`).

### `detect_mobile_operator(phone: str) -> str | None`
Identifies the carrier operator name (`MCI`, `MTN`, `Rightel`, etc.).

### `is_valid_landline(phone: str) -> bool`
Validates Iranian landline numbers against official provincial area codes.

### `detect_landline_province(phone: str) -> str | None`
Identifies the province of an Iranian landline phone number.

### `is_valid_card_number(card: str) -> bool`
Validates 16-digit bank card numbers using the Luhn algorithm.

### `format_card_number(card: str, separator: str = "-") -> str`
Formats a 16-digit card into four 4-digit groups.

### `detect_bank_from_card(card: str) -> str | None`
Identifies the issuing bank based on the first 6 digits (IIN / BIN).

### `is_valid_sheba(sheba: str) -> bool`
Validates an Iranian IBAN (Sheba) using the ISO 7064 Mod 97-10 checksum algorithm.

### `format_sheba(sheba: str, chunk_size: int = 4) -> str`
Formats a Sheba string into readable 4-character blocks.

### `detect_bank_from_sheba(sheba: str) -> str | None`
Detects the bank name from the bank identifier code in the Sheba string.

### `is_valid_postal_code(code: str) -> bool`
Validates 10-digit Iranian postal codes.

### `format_postal_code(code: str) -> str`
Formats a postal code into the standard 5-5 layout (`XXXXX-XXXXX`).

### `is_valid_corporate_id(corp_id: str) -> bool`
Validates 11-digit legal entity corporate registration numbers.

### `is_valid_bill_and_payment(bill_id: str, pay_id: str) -> bool`
Validates utility bill IDs and payment IDs.

### `extract_bill_details(bill_id: str, pay_id: str) -> dict`
Extracts bill type, amount in Rials, and billing period.

### `is_valid_plate(plate: str) -> bool`
Validates Iranian vehicle license plate formats.

### `parse_plate(plate: str) -> dict`
Parses license plate digits, middle letter, and provincial Iran code.

### `detect(text: str) -> str | None`
Automatically detects the data type of the input string (`national_code`, `mobile`, `card`, `sheba`, `email`, `url`, `ip`).
