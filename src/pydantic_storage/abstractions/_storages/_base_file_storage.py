from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Callable, Generic

from pydantic_storage.types import BaseMetaDataDict, T


class BaseFileStorage(ABC, Generic[T]):
    """Abstract base class for file storage."""

    def __init__(
        self,
        file_path: str,
        model_class: type[T],
        metadata: BaseMetaDataDict,
        unique_fields: list[str] | None = None,
    ) -> None:
        """Initialize the AbstractFileStorage."""
        self.file_path: Path = Path(file_path)
        self.model_class: type[T] = model_class
        self.metadata: BaseMetaDataDict = metadata
        self.unique_fields: list[str] = unique_fields or []

    @abstractmethod
    def all(self) -> list[T]:
        """Retrieve all items from the storage."""
        raise NotImplementedError

    @abstractmethod
    def get(self, **kwargs: Any) -> T | None:
        """Retrieve an item by key and value."""
        raise NotImplementedError

    @abstractmethod
    def first(self) -> T | None:
        """Retrieve the first item from the storage."""
        raise NotImplementedError

    @abstractmethod
    def last(self) -> T | None:
        """Retrieve the last item from the storage."""
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
    def next_id(self) -> int:
        """Return next id as for previous recods"""
        raise NotImplementedError

    @abstractmethod
    def create(self, items: list[T]) -> list[T]:
        """Create a new item in the storage."""
        raise NotImplementedError

    @abstractmethod
    def update(self, items: T, **kwargs: Any) -> T:
        """Update item with provided kwargs"""
        raise NotImplementedError

    @abstractmethod
    def filter(self, predicate: Callable[[T], bool]) -> list[T]:
        """Filter items based on a predicate function."""
        raise NotImplementedError

    @abstractmethod
    def delete(self, key: str, value: object) -> bool:
        """Delete an item by key and value."""
        raise NotImplementedError

    @abstractmethod
    def clear(self) -> None:
        """Clear all items from the storage."""
        raise NotImplementedError
