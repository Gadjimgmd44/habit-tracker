class AppException(Exception):
    """Base exception for application errors."""


class EmailAlreadyExist(AppException):
    """Raised on registration when email is already in use."""


class InvalidCredentials(AppException):
    """Raised on login when email or password is wrong."""