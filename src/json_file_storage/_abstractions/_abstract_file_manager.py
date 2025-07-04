from abc import ABC, abstractmethod
from typing import Generic

from json_file_storage.models.typed import JsonFileDict, T


class AbstractFileManager(ABC, Generic[T]):
    """Abstract base class for managing file operations."""

    @abstractmethod
    def exists(self) -> bool:
        """Check if the JSON file exists."""
        raise NotImplementedError

    @abstractmethod
    def read(self) -> JsonFileDict[T]:
        """Read data from a JSON file and return it."""
        raise NotImplementedError

    @abstractmethod
    def write(self, data: T) -> None:
        """Write data to a JSON file."""
        raise NotImplementedError

    @abstractmethod
    def delete(self) -> None:
        """Delete the JSON file."""
        raise NotImplementedError
