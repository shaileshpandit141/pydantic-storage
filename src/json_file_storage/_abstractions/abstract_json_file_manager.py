from abc import ABC, abstractmethod
from typing import Generic

from json_file_storage.models.typed import T


class AbstractJsonFileManager(ABC, Generic[T]):
    """Abstract base class for managing JSON file operations."""

    @abstractmethod
    def read(self) -> T:
        """Read data from a JSON file and return it."""
        ...

    @abstractmethod
    def write(self, data: T) -> None:
        """Write data to a JSON file."""
        ...

    @abstractmethod
    def delete(self) -> None:
        """Delete the JSON file."""
        ...

    @abstractmethod
    def exists(self) -> bool:
        """Check if the JSON file exists."""
        ...
