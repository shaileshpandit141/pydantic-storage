from typing import Any

from pydantic import TypeAdapter, ValidationError
from pydantic.fields import FieldInfo

from pydantic_storage._services import FileManager
from pydantic_storage.abstractions import BaseFileStorage
from pydantic_storage.types._generic_types import T
from pydantic_storage.types._model_dict_types import BaseMetaDataDict


class FileStorage(BaseFileStorage[T]):
    def __init__(
        self,
        file_path: str,
        model_class: type[T],
        metadata: BaseMetaDataDict,
        unique_fields: list[str] | None = None,
    ) -> None:
        """Initialize the JsonFileStorage."""
        super().__init__(file_path, model_class, metadata, unique_fields)
        self.manager = FileManager(file_path, model_class, metadata)

    def all(self) -> list[T]:
        """Retrieve all items from the storage."""
        records = self.manager.read().records
        return list(records.values())

    def __validate_kwargs(self, kwargs: dict[str, Any]) -> None:
        field_list: dict[str, FieldInfo] = self.model_class.model_fields
        for key, value in kwargs.items():
            if key not in field_list:
                raise ValidationError(
                    f"Field '{key}' is not a valid field of the model."
                )

            field_info = field_list[key]
            annotation = field_info.annotation

            # Safe validation using Pydantic TypeAdapter
            try:
                TypeAdapter(annotation).validate_python(value)
            except Exception as _:
                raise ValidationError(
                    f"Value for field '{key}' must be of type {annotation}, got {value!r}"
                )

    def get(self, **kwargs: Any) -> T | None:
        """Retrieve an items baased on key-value pairs."""
        self.__validate_kwargs(kwargs)
        for record in self.all():
            if all(getattr(record, k) == v for k, v in kwargs.items()):
                return record
        return None

    def first(self) -> T | None:
        """Retrieve the first item from the storage."""
        records = self.all()
        if len(records) > 0:
            return records[0]
        return None

    def last(self) -> T | None:
        """Retrieve the last item from the storage."""
        records = self.all()
        if len(records) > 0:
            return records[-1]
        return None

    def count(self) -> int:
        """Count the number of items in the storage."""
        return len(self.all())
