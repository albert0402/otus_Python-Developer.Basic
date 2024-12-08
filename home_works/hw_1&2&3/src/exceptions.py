class PhoneBookError(Exception):
    """
    Base class for all exceptions in the phone book application.
    """
    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message


class FileError(PhoneBookError):
    """
    Raised when there is an issue with file operations.
    """
    def __init__(self, message: str) -> None:
        super().__init__(message)


class ContactError(PhoneBookError):
    """
    Raised for issues related to contacts.
    """
    def __init__(self, message: str) -> None:
        super().__init__(message)