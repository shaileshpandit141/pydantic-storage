from typing import Any

from json_file_storage._abstractions._abstract_pydantic_model_serializer import (
    AbstractPydanticModelSerializer,
)
from json_file_storage.models.typed import RecordDict, T


class PydanticModelSerializer(AbstractPydanticModelSerializer[T]):
    """Concrete implementation of the abstract Pydantic model serializer."""

    def model_to_dict(self) -> RecordDict[Any]:
        """Convert the data structure to a dictionary."""
        return {key: value.model_dump() for key, value in self.data.items()}

    def dict_to_model(self) -> RecordDict[T]:
        """Convert a dictionary to a data model."""
        return {
            key: self.pydantic_model.model_validate(value)
            for key, value in self.data.items()
        }
