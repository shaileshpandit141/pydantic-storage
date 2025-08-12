from pathlib import Path

from pydantic_storage._services import FileManager
from pydantic_storage.abstractions import BaseStorage
from pydantic_storage.abstractions._managers._base_manager import BaseManager
from pydantic_storage.models import MetaData
from pydantic_storage.types._generic_types import T
from pydantic_storage.types._model_dict_types import MetaDataDict


class FileStorage(BaseStorage[T]):
    def __init__(
        self,
        uri: str | Path,
        model: type[T],
        metadata: MetaDataDict,
        unique_fields: list[str] | None = None,
        manager: type[BaseManager[T]] = FileManager,
    ) -> None:
        super().__init__(uri, model, metadata, unique_fields, manager)

    @property
    def uri(self) -> str:
        """Return Current File instance"""
        return self._file.resolve().as_uri()

    @property
    def model(self) -> type[T]:
        """Return Current Model"""
        return self._model

    @property
    def metadata(self) -> MetaData:
        """Return Current Model"""
        return self.manager.metadata

    @property
    def unique_fields(self) -> list[str] | None:
        """Return Current Model"""
        return self._unique_fields

    @property
    def manager(self) -> BaseManager[T]:
        """Return Current manager instance"""
        return FileManager(
            uri=self._file,
            model=self._model,
            metadata=self._metadata,
        )

    @property
    def data(self) -> list[T]:
        """Return all data from storage"""
        return self.manager.data

    def all(self) -> list[T]:
        """Retrieve all items from the storage."""
        return self.manager.data
