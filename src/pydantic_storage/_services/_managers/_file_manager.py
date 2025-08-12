from datetime import datetime, timezone
from pathlib import Path
from typing import Annotated, Literal, get_args, get_origin

from pydantic import TypeAdapter, ValidationError

from pydantic_storage.abstractions import BaseManager
from pydantic_storage.exceptions import FileDataLoadError
from pydantic_storage.models import Data, MetaData, Storage, Timestamp
from pydantic_storage.types import MetaDataDict, T
from pydantic_storage.types._auto_id import AutoIDMarker


class FileManager(BaseManager[T]):
    """A class for managing file operations."""

    def __init__(
        self,
        uri: Path | str,
        model: type[T],
        metadata: MetaDataDict,
    ) -> None:
        super().__init__(uri, model, metadata)

    @property
    def metadata(self) -> MetaData:
        """Return metadata from resource"""
        self.save(action="accessed")
        return self._metadata

    @property
    def data(self) -> list[T]:
        """Return data from resource"""
        self.save(action="accessed")
        return self._data

    def update_timestamps(
        self,
        stored_timestamps: Timestamp,
        field: Literal["created_at", "accessed_at", "modified_at"],
    ) -> None:
        """Update timestamps for resource action"""
        current_timestamps: Timestamp = self._metadata.timestamps

        now = datetime.now(timezone.utc)
        current_timestamps.created_at = stored_timestamps.created_at

        if field == "created_at":
            current_timestamps.accessed_at = stored_timestamps.accessed_at
            current_timestamps.modified_at = stored_timestamps.modified_at
        elif field == "accessed_at":
            current_timestamps.accessed_at = now
            current_timestamps.modified_at = stored_timestamps.modified_at
        else:
            current_timestamps.accessed_at = stored_timestamps.accessed_at
            current_timestamps.modified_at = now

    def update_meradata(self, metadata: MetaData) -> None:
        merged = {**metadata.model_dump(), **self._metadata.model_dump()}
        self._metadata = MetaData(**merged)

    def update_storage(self) -> None:
        """Update storage data"""
        self._metadata.storage = Storage(
            uri=self._file.resolve().as_uri(),
            backend="file",
            format="json",
            encryption="none",
        )

    def combine_unique_data(
        self,
        list1: list[T],
        list2: list[T],
    ) -> list[T]:
        """Combine two lists into one, removing duplicates"""
        combined: list[T] = []
        seen_items: list[T] = []
        for item in list1 + list2:
            if not any(item == seen for seen in seen_items):
                seen_items.append(item)
                combined.append(item)
        return combined

    def save(
        self,
        action: Literal["created", "accessed", "modified"],
        raise_exception: bool = False,
    ) -> None:
        """Save the current state of the resource."""
        try:
            data = self._load()
            # Update current session
            # self._data.extend(data.records)
            self._data = self.combine_unique_data(self._data, data.records)
            self.update_meradata(data.metadata)
            self.update_storage()
            if action == "created":
                self.update_timestamps(data.metadata.timestamps, "created_at")
            elif action == "accessed":
                self.update_timestamps(data.metadata.timestamps, "accessed_at")
            elif action == "modified":
                self.update_timestamps(data.metadata.timestamps, "modified_at")
        except FileDataLoadError as error:
            if raise_exception:
                raise FileDataLoadError(
                    f"Failed to load data from {self._file}:\n{error}"
                ) from error

        # Convert pydnatic model to josn
        json_string: str = Data(
            metadata=self._metadata,
            records=self._data,
        ).model_dump_json(indent=2)
        self._file.write_text(json_string, encoding="utf-8")

    def _create(self) -> None:
        """Create the resource if it does not exist."""
        if not self._file.exists():
            self._file.touch(exist_ok=True)
        self.save(action="created")

    def _load(self) -> Data[T]:
        """Load data from the resource file."""
        json_string: str = self._file.read_text(encoding="utf-8")
        adapter: TypeAdapter[Data[T]] = TypeAdapter(Data[self._model])  # type: ignore

        try:
            data = adapter.validate_json(json_string)
            return data
        except ValidationError as error:
            raise FileDataLoadError(
                f"Failed to load data from {self._file}:\n{error}"
            ) from error

    def next_id(self) -> int:
        """Return next id as for stored records"""
        return len(self._data) + 1

    def write(self, data: list[T]) -> None:
        """Write data to the resource, auto-assigning IDs for AutoID fields."""
        for record in data:
            annotations = getattr(record.__class__, "__annotations__", {})
            for field_name, annotation in annotations.items():
                if get_origin(annotation) is Annotated:
                    args = get_args(annotation)
                    if args[0] is int and any(a is AutoIDMarker for a in args):
                        if getattr(record, field_name) == 0:
                            setattr(record, field_name, self.next_id())
                        break
            self._data.append(record)
        self.save(action="modified")
