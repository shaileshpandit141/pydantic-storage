import json


class JSONDecodeError(Exception):
    """
    Exception raised when JSON decoding fails during file storage operations.

    Attributes:
        original (json.JSONDecodeError): The original exception raised by the json module.

    """

    def __init__(self, original: json.JSONDecodeError) -> None:
        message: str = f"Failed to decode JSON data: {original.msg} (line {original.lineno}, column {original.colno})"
        super().__init__(message)
        self.original: json.JSONDecodeError = original
