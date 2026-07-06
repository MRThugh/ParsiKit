"""
parsikit.exceptions
~~~~~~~~~~~~~~~~~~~
Domain-specific exception classes for ParsiKit infrastructure.
"""

class ParsiKitError(Exception):
    """Base exception for all ParsiKit-related errors."""


class ValidationError(ParsiKitError, ValueError):
    """Raised when data validation fails."""


class InvalidNationalCodeError(ValidationError):
    """Raised when an Iranian National Code is invalid."""


class InvalidMobileError(ValidationError):
    """Raised when an Iranian mobile number is invalid."""


class InvalidCardNumberError(ValidationError):
    """Raised when a bank card number is invalid."""


class InvalidShebaError(ValidationError):
    """Raised when a Sheba (IBAN) is invalid."""


class InvalidPostalCodeError(ValidationError):
    """Raised when a postal code is invalid."""


class InvalidPlateError(ValidationError):
    """Raised when a vehicle license plate is invalid."""


class InvalidBillError(ValidationError):
    """Raised when a bill ID or payment ID is invalid."""