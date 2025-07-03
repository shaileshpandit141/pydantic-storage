from abc import ABC, abstractmethod
from typing import Any, Callable, Generic

from json_file_storage.models.typed import T


class AbstractJsonFileStorage(ABC, Generic[T]):
    """Abstract base class for JSON file storage."""

    @abstractmethod
    def all(self) -> list[T]:
        """Retrieve all items from the storage."""
        raise NotImplementedError

    @abstractmethod
    def get(self, key: str, value: object) -> T | None:
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
    def exists(self, key: str, value: object) -> bool:
        """Check if an item exists by key and value."""
        raise NotImplementedError

    @abstractmethod
    def create(self, item: T) -> None:
        """Create a new item in the storage."""
        raise NotImplementedError

    @abstractmethod
    def bulk_create(
        self,
        items: list[T],
        *,
        skip_duplicates: bool = True,
    ) -> list[T]:
        """Create multiple items in the storage."""
        raise NotImplementedError

    @abstractmethod
    def update(
        self,
        key: str,
        value: object,
        update_func: Callable[[T], T],
    ) -> bool:
        """Update an item by key and value using a provided function."""
        raise NotImplementedError

    @abstractmethod
    def update_partial(
        self,
        key: str,
        value: object,
        update_fields: dict[str, Any],
    ) -> bool:
        """Partially update an item by key and value."""
        raise NotImplementedError

    @abstractmethod
    def filter(self, predicate: Callable[[T], bool]) -> list[T]:
        """Filter items based on a predicate function."""
        raise NotImplementedError

    @abstractmethod
    def refresh(self) -> list[T]:
        """Refresh the storage and return all items."""
        raise NotImplementedError

    @abstractmethod
    def delete(self, key: str, value: object) -> bool:
        """Delete an item by key and value."""
        raise NotImplementedError

    @abstractmethod
    def clear(self) -> None:
        """Clear all items from the storage."""
        raise NotImplementedError
