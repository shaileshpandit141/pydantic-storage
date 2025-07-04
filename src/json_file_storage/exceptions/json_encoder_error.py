import json


class JSONEncoderError(Exception):
    """
    Exception raised when JSON encoding fails during file storage operations.

    Attributes:
        original (json.JSONEncoder): The original exception raised by the json module.

    """

    def __init__(self, original: json.JSONEncoder) -> None:
        message: str = "Failed to encode JSON data"
        super().__init__(message)
        self.original: json.JSONEncoder = original
