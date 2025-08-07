from pathlib import Path

from pydantic import TypeAdapter, ValidationError

from pydantic_storage.abstractions import BaseManager
from pydantic_storage.models import Data
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
