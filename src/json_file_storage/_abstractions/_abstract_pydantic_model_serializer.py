from abc import ABC, abstractmethod
from typing import Any, Generic

from json_file_storage.models.typed import T


class AbstractPydanticModelSerializer(ABC, Generic[T]):
    """Abstract base class for data serializers that manage data serialization and deserialization."""

    def __init__(self, data: dict[str, T]) -> None:
        """Initialize the abstract data serializer."""
        self.data: dict[str, T] = data

    @abstractmethod
    def moedl_to_dict(self) -> dict[str, Any]:
        """
        Convert the data structure to a dictionary.

        Returns:
            dict[str, Any]: A dictionary representation of the data structure.

        """
        raise NotImplementedError

    @abstractmethod
    def dict_to_model(self) -> dict[str, T]:
        """
        Convert a dictionary to a data model.

        Returns:
            dict[str, T]: A dictionary containing data models.

        """
        raise NotImplementedError
