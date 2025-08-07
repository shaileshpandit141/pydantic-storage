from abc import ABC, abstractmethod
from pathlib import Path
from typing import Generic

from pydantic_storage.models import MetaData
from pydantic_storage.types import MetaDataDict, T


class BaseManager(ABC, Generic[T]):
    """Abstract base class for managing file operations."""

    def __init__(
        self,
        uri: Path | str,
        model_class: type[T],
        metadata: MetaDataDict,
        data: list[T],
    ) -> None:
        """Initialize the JsonFileManager."""
        self._file = uri if isinstance(uri, Path) else Path(uri)
        self._model_class = model_class
        self._metadata: MetaData = MetaData(**metadata)
        self._data = data
        self._create()
        self._load()

    @property
    @abstractmethod
    def metadata(self) -> MetaData:
        """Return all metadata"""
        raise NotImplementedError

    @property
    @abstractmethod
    def data(self) -> list[T]:
        """Return all data"""
        raise NotImplementedError

    @abstractmethod
    def _create(self) -> None:
        """Create the resource if it does not exist."""
        raise NotImplementedError

    @abstractmethod
    def _load(self) -> None:
        """Load data from the resource."""
        raise NotImplementedError

    @abstractmethod
    def save(self) -> None:
        """Save the current state of the resource."""
        raise NotImplementedError

    @abstractmethod
    def write(self, data: list[T]) -> None:
        """Write data to the resource."""
        raise NotImplementedError
