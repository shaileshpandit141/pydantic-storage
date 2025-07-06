from abc import ABC, abstractmethod
from typing import Any, Generic

from json_file_storage.models.typed import RecordDict, T


class AbstractPydanticModelSerializer(ABC, Generic[T]):
    """Abstract base class for data serializers that manage data serialization and deserialization."""

    def __init__(self, data: RecordDict[T]) -> None:
        """Initialize the abstract data serializer."""
        self.data: RecordDict[T] = data

    @abstractmethod
    def moedl_to_dict(self) -> RecordDict[Any]:
        """
        Convert the data structure to a dictionary.

        Returns:
            RecordDict[Any]: A dictionary representation of the data structure.

        """
        raise NotImplementedError

    @abstractmethod
    def dict_to_model(self) -> RecordDict[T]:
        """
        Convert a dictionary to a data model.

        Returns:
            RecordDict[T]: A dictionary containing data models.

        """
        raise NotImplementedError
