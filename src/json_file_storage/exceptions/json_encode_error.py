class JSONEncodeError(Exception):
    """
    Exception raised when JSON encoding fails during file storage operations.

    Attributes:
        original (TypeError): The original exception raised by the python.

    """

    def __init__(self, original: TypeError) -> None:
        message: str = "Failed to encode JSON data"
        super().__init__(message)
        self.original: TypeError = original
