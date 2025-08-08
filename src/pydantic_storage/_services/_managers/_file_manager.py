from datetime import datetime, timezone
from pathlib import Path

from pydantic import TypeAdapter

from pydantic_storage.abstractions import BaseManager
from pydantic_storage.exceptions import FileDataLoadError
from pydantic_storage.models import Data, MetaData, Storage
from pydantic_storage.types import MetaDataDict, T


class FileManager(BaseManager[T]):
    """A class for managing file operations."""

    def __init__(
        self,
        uri: Path | str,
        model_class: type[T],
        metadata: MetaDataDict,
    ) -> None:
        super().__init__(uri, model_class, metadata)

    @property
    def metadata(self) -> MetaData:
        """Return metadata from resource"""
        return self._metadata

    @property
    def data(self) -> list[T]:
        """Return data from resource"""
        return self._data

    def save(self, raise_exception: bool = False) -> bool:
        """Save the current state of the resource."""
        json_string: str = self._file.read_text(encoding="utf-8")
        adapter: TypeAdapter[Data[T]] = TypeAdapter(Data[self._model_class])  # type: ignore

        try:
            data = adapter.validate_json(json_string)
            merged = {**data.metadata.model_dump(), **self._metadata.model_dump()}
            self._metadata = MetaData(**merged)
            if self._metadata.timestamps:
                self._metadata.timestamps.created_at = (
                    data.metadata.timestamps.created_at
                )
                self._metadata.timestamps.updated_at = datetime.now(timezone.utc)

            self._metadata.storage = Storage(
                type="file",
                format="json",
                encryption="utf-8",
            )
        except Exception as error:
            if raise_exception:
                raise FileDataLoadError(
                    f"Failed to load data from {self._file}:\n{error}"
                ) from error
            else:
                return False

        loaded_json_string: str = Data(
            metadata=self.metadata,
            records=self._data,
        ).model_dump_json(indent=2)
        self._file.write_text(loaded_json_string, encoding="utf-8")
        return True

    def _create(self) -> None:
        """Create the resource if it does not exist."""
        if not self._file.exists():
            self._file.touch(exist_ok=True)
        self.save()

    def _load(self) -> None:
        """Load data from the resource file."""
        json_string: str = self._file.read_text(encoding="utf-8")
        adapter: TypeAdapter[Data[T]] = TypeAdapter(Data[self._model_class])  # type: ignore

        try:
            data = adapter.validate_json(json_string)
            self._data = data.records
            self._metadata = data.metadata
        except Exception as error:
            raise FileDataLoadError(
                f"Failed to load data from {self._file}:\n{error}"
            ) from error

    def write(self, data: list[T]) -> None:
        """Write data to the resource."""
        self._data.extend(data)
        self.save()
