"""
parsikit.models
~~~~~~~~~~~~~~~
Object-oriented Domain Models wrapping standard Persian data structures.
Provides rich properties, metadata extraction, validation, and auto-formatting.
"""

from __future__ import annotations
from typing import Literal, Any, TYPE_CHECKING
    
from parsikit.validators import (
    is_valid_national_code, format_national_code, detect_national_code_location,
    is_valid_mobile, normalize_mobile, detect_mobile_operator,
    is_valid_landline, normalize_landline, detect_landline_province,
    is_valid_card_number, format_card_number, detect_bank_from_card,
    is_valid_sheba, format_sheba, detect_bank_from_sheba, extract_account_number_from_sheba,
    is_valid_postal_code, format_postal_code, parse_plate, format_plate
)
from parsikit.text import (
    standardize_persian, beautify_persian_spacing, strip_diacritics,
    correct_keyboard_layout, extract_mobiles, extract_national_codes, words_to_number
)
from parsikit.exceptions import (
    InvalidNationalCodeError, InvalidMobileError, InvalidCardNumberError,
    InvalidShebaError, InvalidPostalCodeError, InvalidPlateError, ValidationError
)

_TO_ENGLISH = str.maketrans("۰۱۲۳۴۵۶۷۸۹٠١٢٣٤٥٦٧٨٩", "01234567890123456789")

if TYPE_CHECKING:
    from parsikit.validators import BankDetails, PlateDetails


class StringLikeMixin:
    """Provides complete string-like duck typing to domain models for absolute ease of use."""
    def __len__(self) -> int:
        return len(str(self))

    def __getitem__(self, key: int | slice) -> str:
        return str(self)[key]

    def __contains__(self, item: str) -> bool:
        return item in str(self)

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, self.__class__):
            return str(self) == str(other)
        return str(self) == str(other)

    def __hash__(self) -> int:
        return hash(str(self))


class PydanticValidationMixin:
    """Enables native Pydantic v2 validation and serialization directly from raw types."""
    @classmethod
    def _validate_pydantic(cls, v: Any) -> Any:
        if isinstance(v, cls):
            return v
        try:
            return cls(str(v))
        except Exception as e:
            raise ValueError(str(e)) from None

    @classmethod
    def __get_pydantic_core_schema__(cls, source_type: Any, handler: Any) -> Any:
        try:
            from pydantic_core import core_schema
            return core_schema.json_or_python_schema(
                json_schema=core_schema.str_schema(),
                python_schema=core_schema.general_plain_validator_function(cls._validate_pydantic),
                serialization=core_schema.plain_serializer_function_ser_schema(lambda v: str(v))
            )
        except ImportError:
            return {}


class PersianText(StringLikeMixin, PydanticValidationMixin):
    """Rich object wrapper representing a Persian text string, allowing chained transformations."""
    def __init__(self, text: str) -> None:
        self._text = str(text)

    @property
    def raw(self) -> str:
        """Get raw original text."""
        return self._text

    def standardize(self, strip_diacritics_opt: bool = False) -> PersianText:
        """Normalize and standardize Persian text layout, character codes, and spaces."""
        return PersianText(standardize_persian(self._text, strip_diacritics_opt=strip_diacritics_opt))

    def beautify(self) -> PersianText:
        """Optimize and beautify spaces around Persian punctuation and symbols."""
        return PersianText(beautify_persian_spacing(self._text))

    def strip_diacritics(self) -> PersianText:
        """Remove Arabic/Persian diacritics."""
        return PersianText(strip_diacritics(self._text))

    def correct_layout(self) -> PersianText:
        """Translate mistyped English layout into Persian."""
        return PersianText(correct_keyboard_layout(self._text))

    def extract_mobiles(self) -> list[str]:
        """Scrape all unique valid mobile numbers from the text."""
        return extract_mobiles(self._text)

    def extract_national_codes(self) -> list[str]:
        """Scrape all unique valid national codes from the text."""
        return extract_national_codes(self._text)

    def to_number(self) -> int:
        """Convert this Persian textual number into an integer."""
        return words_to_number(self._text)

    def __add__(self, other: Any) -> PersianText:
        return PersianText(str(self) + str(other))

    def __radd__(self, other: Any) -> PersianText:
        return PersianText(str(other) + str(self))

    def __str__(self) -> str:
        return self._text

    def __repr__(self) -> str:
        return f"PersianText('{self._text}')"


class NationalCode(StringLikeMixin, PydanticValidationMixin):
    """Rich value object representing an Iranian National Code (کد ملی)."""
    def __init__(self, code: str, strict: bool = True) -> None:
        self._raw = str(code)
        self._clean = "".join(c for c in self._raw.translate(_TO_ENGLISH) if c.isdigit()).zfill(10)
        
        self._is_valid = is_valid_national_code(self._clean)
        if strict and not self._is_valid:
            raise InvalidNationalCodeError(f"The national code '{self._raw}' is invalid.")

    @property
    def raw(self) -> str:
        return self._raw

    @property
    def clean(self) -> str:
        return self._clean

    @property
    def is_valid(self) -> bool:
        return self._is_valid

    @property
    def formatted(self) -> str:
        """Standard XXX-XXXXXX-X layout."""
        return format_national_code(self._clean)

    @property
    def location(self) -> dict[str, str] | None:
        """Retrieve the issuing province and city/county of the national code."""
        return detect_national_code_location(self._clean)

    def to_dict(self) -> dict[str, Any]:
        """Export all metadata metrics into a standardized dictionary."""
        return {
            "raw": self._raw,
            "clean": self._clean,
            "is_valid": self._is_valid,
            "formatted": self.formatted,
            "location": self.location
        }

    def dict(self) -> dict[str, Any]:
        """Alias for to_dict() serialization."""
        return self.to_dict()

    def __str__(self) -> str:
        return self._clean

    def __repr__(self) -> str:
        return f"NationalCode(code='{self._clean}', is_valid={self._is_valid})"


class MobileNumber(StringLikeMixin, PydanticValidationMixin):
    """Rich domain model representing an Iranian mobile phone number."""
    def __init__(self, phone: str, strict: bool = True) -> None:
        self._raw = str(phone)
        self._is_valid = is_valid_mobile(self._raw)
        if strict and not self._is_valid:
            raise InvalidMobileError(f"The mobile number '{self._raw}' is invalid.")
            
        self._clean = "".join(c for c in self._raw.translate(_TO_ENGLISH) if c.isdigit())
        self._base = self._clean[-10:] if self._is_valid or len(self._clean) >= 10 else self._clean

    @property
    def raw(self) -> str:
        return self._raw

    @property
    def is_valid(self) -> bool:
        return self._is_valid

    @property
    def operator(self) -> str | None:
        """Detect and return mobile operator name."""
        return detect_mobile_operator(self._raw)

    def to_national(self) -> str:
        """Return format like 09123456789."""
        return f"0{self._base}"

    def to_international(self) -> str:
        """Return format like +989123456789."""
        return f"+98{self._base}"

    def to_dict(self) -> dict[str, Any]:
        """Export all mobile properties into a standardized dictionary."""
        return {
            "raw": self._raw,
            "is_valid": self._is_valid,
            "national": self.to_national(),
            "international": self.to_international(),
            "operator": self.operator
        }

    def dict(self) -> dict[str, Any]:
        """Alias for to_dict() serialization."""
        return self.to_dict()

    def __str__(self) -> str:
        return self.to_national()

    def __repr__(self) -> str:
        return f"MobileNumber(phone='{self.to_national()}', is_valid={self._is_valid})"


class FixedLine(StringLikeMixin, PydanticValidationMixin):
    """Rich domain model representing an Iranian fixed landline phone number."""
    def __init__(self, phone: str, strict: bool = True) -> None:
        self._raw = str(phone)
        self._is_valid = is_valid_landline(self._raw)
        if strict and not self._is_valid:
            raise ValidationError(f"The fixed landline phone number '{self._raw}' is invalid.")
            
        self._clean = "".join(c for c in self._raw.translate(_TO_ENGLISH) if c.isdigit())
        self._base = self._clean[-10:] if self._is_valid or len(self._clean) >= 10 else self._clean

    @property
    def raw(self) -> str:
        return self._raw

    @property
    def is_valid(self) -> bool:
        return self._is_valid

    @property
    def province(self) -> str | None:
        """Get issuing province name."""
        return detect_landline_province(self._raw)

    @property
    def area_code(self) -> str:
        """Get the 3-digit area code (e.g. '021')."""
        return f"0{self._base[:2]}"

    def to_national(self) -> str:
        """Return format like 02188888888."""
        return f"0{self._base}"

    def to_international(self) -> str:
        """Return format like +982188888888."""
        return f"+98{self._base}"

    def to_dict(self) -> dict[str, Any]:
        """Export all landline properties into a standardized dictionary."""
        return {
            "raw": self._raw,
            "is_valid": self._is_valid,
            "national": self.to_national(),
            "international": self.to_international(),
            "province": self.province,
            "area_code": self.area_code
        }

    def dict(self) -> dict[str, Any]:
        """Alias for to_dict() serialization."""
        return self.to_dict()

    def __str__(self) -> str:
        return self.to_national()

    def __repr__(self) -> str:
        return f"FixedLine(phone='{self.to_national()}', is_valid={self._is_valid})"


class BankCard(StringLikeMixin, PydanticValidationMixin):
    """Rich representation of an Iranian 16-digit Bank Card."""
    def __init__(self, card: str, strict: bool = True) -> None:
        self._raw = str(card)
        self._clean = "".join(c for c in self._raw.translate(_TO_ENGLISH) if c.isdigit())
        
        self._is_valid = is_valid_card_number(self._clean)
        if strict and not self._is_valid:
            raise InvalidCardNumberError(f"The bank card number '{self._raw}' is invalid.")

    @property
    def raw(self) -> str:
        return self._raw

    @property
    def clean(self) -> str:
        return self._clean

    @property
    def is_valid(self) -> bool:
        return self._is_valid

    @property
    def formatted(self) -> str:
        """Get 4-chunk formatted card layout."""
        return format_card_number(self._clean)

    @property
    def bank(self) -> BankDetails | None:
        """Retrieve the bank details of this card."""
        return detect_bank_from_card(self._clean)

    def to_dict(self) -> dict[str, Any]:
        """Export all bank card properties into a standardized dictionary."""
        return {
            "raw": self._raw,
            "clean": self._clean,
            "is_valid": self._is_valid,
            "formatted": self.formatted,
            "bank": self.bank
        }

    def dict(self) -> dict[str, Any]:
        """Alias for to_dict() serialization."""
        return self.to_dict()

    def __str__(self) -> str:
        return self._clean

    def __repr__(self) -> str:
        return f"BankCard(card='{self._clean}', is_valid={self._is_valid})"


class Sheba(StringLikeMixin, PydanticValidationMixin):
    """Rich domain object representing an Iranian Sheba (IBAN) code."""
    def __init__(self, sheba: str, strict: bool = True) -> None:
        self._raw = str(sheba)
        clean_str = "".join(c for c in self._raw.translate(_TO_ENGLISH).upper() if c.isalnum())
        if len(clean_str) == 24 and clean_str.isdigit():
            clean_str = "IR" + clean_str
        self._clean = clean_str

        self._is_valid = is_valid_sheba(self._clean)
        if strict and not self._is_valid:
            raise InvalidShebaError(f"The Sheba code '{self._raw}' is invalid.")

    @property
    def raw(self) -> str:
        return self._raw

    @property
    def clean(self) -> str:
        return self._clean

    @property
    def is_valid(self) -> bool:
        return self._is_valid

    @property
    def formatted(self) -> str:
        return format_sheba(self._clean, format_type="spaced")

    @property
    def bank(self) -> BankDetails | None:
        return detect_bank_from_sheba(self._clean)

    @property
    def account_number(self) -> str:
        """Extract the clean embedded bank account number from this Sheba."""
        return extract_account_number_from_sheba(self._clean)

    def to_dict(self) -> dict[str, Any]:
        """Export all Sheba properties into a standardized dictionary."""
        return {
            "raw": self._raw,
            "clean": self._clean,
            "is_valid": self._is_valid,
            "formatted": self.formatted,
            "bank": self.bank,
            "account_number": self.account_number
        }

    def dict(self) -> dict[str, Any]:
        """Alias for to_dict() serialization."""
        return self.to_dict()

    def __str__(self) -> str:
        return self._clean

    def __repr__(self) -> str:
        return f"Sheba(sheba='{self._clean}', is_valid={self._is_valid})"


class VehiclePlate(StringLikeMixin, PydanticValidationMixin):
    """Rich object modeling an Iranian National Vehicle License Plate (پلاک ملی)."""
    def __init__(self, plate: str, strict: bool = True) -> None:
        self._raw = str(plate)
        self._details = parse_plate(self._raw)
        
        if strict and self._details is None:
            raise InvalidPlateError(f"The license plate structure '{self._raw}' is invalid.")

    @property
    def raw(self) -> str:
        return self._raw

    @property
    def is_valid(self) -> bool:
        return self._details is not None

    @property
    def province(self) -> str:
        return self._details["province"] if self._details else "نامشخص"

    @property
    def province_code(self) -> str:
        return self._details["province_code"] if self._details else ""

    @property
    def category(self) -> str:
        return self._details["category"] if self._details else "نامشخص"

    @property
    def formatted(self) -> str:
        return format_plate(self._raw, format_type="readable") if self._details else self._raw

    @property
    def details(self) -> PlateDetails | None:
        return self._details

    def to_dict(self) -> dict[str, Any]:
        """Export all vehicle plate properties into a standardized dictionary."""
        return {
            "raw": self._raw,
            "is_valid": self.is_valid,
            "formatted": self.formatted,
            "province": self.province,
            "province_code": self.province_code,
            "category": self.category,
            "details": self.details
        }

    def dict(self) -> dict[str, Any]:
        """Alias for to_dict() serialization."""
        return self.to_dict()

    def __str__(self) -> str:
        if self._details:
            return f"{self._details['part1']}{self._details['letter']}{self._details['part2']}{self._details['province_code']}"
        return self._raw

    def __repr__(self) -> str:
        return f"VehiclePlate(plate='{str(self)}', is_valid={self.is_valid})"