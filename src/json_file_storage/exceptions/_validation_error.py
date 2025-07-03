from pydantic import ValidationError as PydanticValidationError


class ValidationError(Exception):
    """Raised when an update results in invalid data per Pydantic validation."""

    def __init__(self, original: PydanticValidationError) -> None:
        super().__init__(f"Invalid update data: {original}")
        self.original = original
