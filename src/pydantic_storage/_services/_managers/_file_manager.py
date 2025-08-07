from datetime import datetime, timezone
from pathlib import Path

from pydantic import TypeAdapter, ValidationError

from pydantic_storage.abstractions import BaseManager
from pydantic_storage.models import Data, MetaData
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

    def save(self) -> None:
        """Save the current state of the resource."""
        if hasattr(self._metadata.timestamps, "updated_at"):
            setattr(
                self._metadata.timestamps,
                "updated_at",
                datetime.now(timezone.utc),
            )

        json_string: str = Data(
            metadata=self._metadata,
            records=self._data,
        ).model_dump_json()
        self._file.write_text(json_string, encoding="utf-8")

    def _create(self) -> None:
        """Create the resource if it does not exist."""
        if not self._file.exists():
            self._file.touch(exist_ok=True)
        self.save()

    def _load(self) -> None:
        """Load data from the resource file."""
        json_string: str = self._file.read_text(encoding="utf-8")
        adapter: TypeAdapter[Data[T]] = TypeAdapter(Data[self._model_class])

        try:
            data = adapter.validate_json(json_string)
            self._data = data.records
            self._metadata = data.metadata
        except Exception as error:
            raise ValidationError(
                f"Failed to load data from \n{self._file}: \n{error}"
            ) from error

    def write(self, data: list[T]) -> None:
        """Write data to the resource."""
        self._data.extend(data)
        self.save()
