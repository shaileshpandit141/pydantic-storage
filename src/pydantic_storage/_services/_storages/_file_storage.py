from pathlib import Path
from typing import Any

from pydantic_storage._services import FileManager
from pydantic_storage.abstractions import BaseStorage
from pydantic_storage.abstractions._managers._base_manager import BaseManager
from pydantic_storage.core import check_model_kwargs
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

    def get(self, **kwargs: Any) -> T | None:
        """Retrieve an item by key and value."""
        check_model_kwargs(self.model, kwargs=kwargs)
        for index, model in enumerate(self.data):
            model_dict = model.model_dump()
            if all([model_dict[key] == value for key, value in kwargs.items()]):
                return self.data[index]
        return None

    def count(self) -> int:
        """Count the number of items in the storage."""
        return len(self.data)

    def exists(self, **kwargs: Any) -> bool:
        """Check if an item exists by key and value."""
        check_model_kwargs(self.model, kwargs=kwargs)
        for model in self.data:
            model_dict = model.model_dump()
            if all([model_dict[key] == value for key, value in kwargs.items()]):
                return True
        return False

    def create(self, data: list[T]) -> list[T]:
        """Create a new item in the data storage."""
        self.manager.write(data=data)
        return data

    def filter(self, **kwargs: Any) -> list[T]:
        """Filter items based on kwargs"""
        check_model_kwargs(self.model, kwargs=kwargs)
        filter_list: list[T] = []
        for index, model in enumerate(self.data):
            model_dict = model.model_dump()
            if all([model_dict[key] == value for key, value in kwargs.items()]):
                filter_list.append(self.data[index])
        return filter_list

    def delete(self, **kwargs: Any) -> T | None:
        """Delete an items based on kwargs"""
        check_model_kwargs(self.model, kwargs=kwargs)
        for index, model in enumerate(self.data):
            model_dict = model.model_dump()
            if all([model_dict[key] == value for key, value in kwargs.items()]):
                try:
                    deleted_item: T = self.data.pop(index)
                    self.manager.save(action="modified")
                    return deleted_item
                except IndexError:
                    return None
        return None
