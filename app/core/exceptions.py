class AppException(Exception):
    """Base exception for application errors."""


class EmailAlreadyExists(AppException):
    """Raised on registration when email is already in use."""


class InvalidCredentials(AppException):
    """Raised on login when email or password is wrong."""

class NotFoundException(AppException):
    """Raised when a requested resource is not found."""

class NotScheduledTodayException(AppException):
    """Raised if the habit isn't Scheduled today"""

class AlreadyCompletedException(AppException):
    """Raised if the habit is already done"""