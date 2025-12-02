class DomainError(Exception):
    """Base class for domain errors."""

class DuplicateEmail(DomainError):
    """Raised when an email must be unique but already exists."""


class DuplicatePhone(DomainError):
    """Raised when a phone number must be unique but already exists."""

class NotFound(DomainError):
    """Raised when a resource cannot be found."""

class InvalidPasswordLength(DomainError):
    """Raised when a provided password exceeds allowed length for the hasher."""
