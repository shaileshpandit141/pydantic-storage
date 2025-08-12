from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Generic

from pydantic_storage._services import FileManager
from pydantic_storage.abstractions import BaseManager
from pydantic_storage.models import MetaData
from pydantic_storage.types import MetaDataDict, T


class BaseStorage(ABC, Generic[T]):
    """Abstract base class for data storage."""

    def __init__(
        self,
        uri: str | Path,
        model: type[T],
        metadata: MetaDataDict,
        unique_fields: list[str] | None = None,
        manager: type[BaseManager[T]] = FileManager,
    ) -> None:
        """Initialize the AbstractFileStorage."""
        self._file = uri if isinstance(uri, Path) else Path(uri)
        self._model = model
        self._metadata = metadata
        self._unique_fields = unique_fields or []
        self._manager = manager

    @property
    @abstractmethod
    def uri(self) -> str:
        """Return Current File instance"""
        raise NotImplementedError

    @property
    @abstractmethod
    def model(self) -> type[T]:
        """Return Current Model"""
        raise NotImplementedError

    @property
    @abstractmethod
    def metadata(self) -> MetaData:
        """Return Current Model"""
        raise NotImplementedError

    @property
    @abstractmethod
    def unique_fields(self) -> list[str] | None:
        """Return Current Model"""
        raise NotImplementedError

    @property
    @abstractmethod
    def manager(self) -> BaseManager[T]:
        """Return Current manager instance"""
        raise NotImplementedError

    @property
    @abstractmethod
    def data(self) -> list[T]:
        """Return all data from storage"""
        raise NotImplementedError

    @abstractmethod
    def all(self) -> list[T]:
        """Retrieve all items from the storage."""
        raise NotImplementedError

    @abstractmethod
    def get(self, **kwargs: Any) -> T | None:
        """Retrieve an item by key and value."""
        raise NotImplementedError

    @abstractmethod
    def count(self) -> int:
        """Count the number of items in the storage."""
        raise NotImplementedError

    @abstractmethod
    def exists(self, **kwargs: Any) -> bool:
        """Check if an item exists by key and value."""
        raise NotImplementedError

    @abstractmethod
    def create(self, data: list[T]) -> list[T]:
        """Create a new item in the data storage."""
        raise NotImplementedError

    @abstractmethod
    def filter(self, **kwargs: Any) -> list[T]:
        """Filter items based on kwargs"""
        raise NotImplementedError

    @abstractmethod
    def delete(self, **kwargs: Any) -> T:
        """Delete an items based on kwargs"""
        raise NotImplementedError

    @abstractmethod
    def clear(self) -> bool:
        """Clear all items from the data storage."""
        raise NotImplementedError
