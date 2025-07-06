from abc import ABC, abstractmethod
from pathlib import Path
from typing import Generic

from json_file_storage.models.typed import FileDict, T


class AbstractFileManager(ABC, Generic[T]):
    """Abstract base class for managing file operations."""

    def __init__(
        self, file_path: str, pydantic_model: type[T], initial_data: FileDict[T]
    ) -> None:
        """Initialize the JsonFileManager."""
        self.file: Path = Path(file_path)
        self.pydantic_model: type[T] = pydantic_model
        self.initial_data: FileDict[T] = initial_data

    @abstractmethod
    def exists(self) -> bool:
        """Check if the JSON file exists."""
        raise NotImplementedError

    @abstractmethod
    def create(self) -> None:
        """Create a new JSON file if it does not exist."""
        raise NotImplementedError

    @abstractmethod
    def read(self) -> FileDict[T]:
        """Read data from a JSON file and return it."""
        raise NotImplementedError

    @abstractmethod
    def write(self, data: FileDict[T]) -> None:
        """Write data to a JSON file."""
        raise NotImplementedError

    @abstractmethod
    def delete(self) -> None:
        """Delete the JSON file."""
        raise NotImplementedError
