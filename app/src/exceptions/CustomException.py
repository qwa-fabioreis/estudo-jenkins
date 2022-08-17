# define Python user-defined exceptions
class Error(Exception):
    """Base class for other exceptions"""
    pass


class NotSupportedException(Error):
    """Raised when the input is not supported yet"""
    def __init__(self, code: int, message: str):
        self.code = code
        self.message = message
    pass

