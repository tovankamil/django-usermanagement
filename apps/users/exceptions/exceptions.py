# apps/users/exceptions.py


# Repository Layer Exceptions
class DatabaseException(Exception):
    """Exception for general database errors from repository"""

    pass


class NotFoundException(Exception):
    """Exception for data not found in repository"""

    pass


class DuplicateEntryException(Exception):
    """Exception for database constraint violations"""

    pass


# Service Layer / Domain Exceptions
class UserServiceException(Exception):
    """Base exception for service layer"""

    pass


class ValidationException(UserServiceException):
    """Exception for input validation failure"""

    pass


class UserNotFoundException(UserServiceException):
    """Exception when user is not found"""

    pass


class EmailAlreadyExistsException(UserServiceException):
    """Exception when email is already registered"""

    pass


class UsernameAlreadyExistsException(UserServiceException):
    """Exception when username is already registered"""

    pass
