from pydantic_storage.abstractions import AbstractBaseFileStorage
from pydantic_storage._services import BaseFileManager
from pydantic_storage.types._generic_types import T
from pydantic_storage.types._model_dict_types import BaseMetaDataDict


class BaseFileStorage(AbstractBaseFileStorage[T]):
    def __init__(
        self,
        file_path: str,
        model_class: type[T],
        metadata: BaseMetaDataDict,
        unique_fields: list[str] | None = None,
    ) -> None:
        """Initialize the JsonFileStorage."""
        super().__init__(file_path, model_class, metadata, unique_fields)
        self.manager = BaseFileManager(file_path, model_class, metadata)

    def all(self) -> list[T]:
        """Retrieve all items from the storage."""
        records = self.manager.read().records
        return list(records.values())
