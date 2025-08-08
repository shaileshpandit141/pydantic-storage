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
        auto_id_field: str | None = None,
    ) -> None:
        """Initialize the JsonFileManager."""
        self._file = uri if isinstance(uri, Path) else Path(uri)
        self._model_class = model_class
        self._metadata: MetaData = MetaData(**metadata)
        self._data: list[T] = []
        self._auto_id_field = auto_id_field
        self._create()
        self._load()

    @property
    @abstractmethod
    def metadata(self) -> MetaData:
        """Return metadata from resource"""
        raise NotImplementedError

    @property
    @abstractmethod
    def data(self) -> list[T]:
        """Return data from resource"""
        raise NotImplementedError

    @abstractmethod
    def save(self, raise_exception: bool = False) -> bool:
        """Save the current state of the resource."""
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
    def next_id(self) -> int:
        """Return next id as for stored records"""
        raise NotImplementedError

    @abstractmethod
    def write(self, data: list[T]) -> None:
        """Write data to the resource."""
        raise NotImplementedError
