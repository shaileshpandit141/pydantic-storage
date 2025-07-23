from datetime import datetime
from pathlib import Path

from pydantic import TypeAdapter

from json_file_storage._abstractions._abstract_file_manager import AbstractFileManager
from json_file_storage.models.pydantic import FileData, Timestamp, now_utc
from json_file_storage.models.typed import (
    BaseMetaDataDict,
    FileDataDict,
    RecordsDict,
    T,
)


class JsonFileManager(AbstractFileManager[T]):
    """A class for managing JSON file operations."""

    def __init__(
        self,
        file_path: str,
        model_class: type[T],
        metadata: BaseMetaDataDict,
    ) -> None:
        """Call parent initializer"""
        super().__init__(file_path, model_class, metadata)

        # Create empty file
        if not self.exists():
            self.create()

        # Initialize file with default content
        self.file_initializer()

    def exists(self) -> bool:
        """
        Check if the JSON file exists.

        Returns:
            bool: True if the file exists, False otherwise.

        """
        return self.file_path.exists()

    def is_file_size_zero(self) -> bool:
        """To Check file size is zero or not"""
        return self.file_path.stat().st_size == 0

    def file_initializer(self) -> None:
        """Initialize file with default content"""

        # Create default file data structure with it's values
        file_meta_data_dict: FileDataDict[T] = {
            "metadata": {
                **self.metadata,
                "storage": {
                    "type": "file",
                    "encryption": "none",
                },
                "timestamps": {
                    "created_at": now_utc(),
                    "updated_at": now_utc(),
                },
            },
            "records": {},
        }

        # Validate all provided data as for model
        current_data: FileData[T] = FileData(**file_meta_data_dict)  # type: ignore

        # Get Stored Data and Update timestamps
        if not self.is_file_size_zero():
            stored_data: FileData[T] = self.read()
            current_data.metadata.timestamps = self.update_timestamps(
                timestamps=stored_data.metadata.timestamps
            )

        # Write Json string to stored file.
        self.file_path.write_text(
            f"{current_data.model_dump_json(indent=2)}\n",
        )

    def create(self) -> None:
        """
        Create a new JSON file if it does not exist.

        Returns:
            None

        """
        # Create parent directories if they don't exist
        if self.file_path.parent != Path():
            self.file_path.parent.mkdir(parents=True, exist_ok=True)

        # Create the file (or update timestamp if it exists)
        self.file_path.touch(exist_ok=True)

    def read(self) -> FileData[T]:
        """
        Read data from a JSON file and return it.

        Returns:
            FileDict[T]: The data read from the JSON file.

        """
        file_data_text: str = self.file_path.read_text(encoding="utf-8")
        adapter: TypeAdapter[FileData[T]] = TypeAdapter(FileData[self.model_class])
        return adapter.validate_json(file_data_text)

    def write(self, data: RecordsDict[T]) -> None:
        """
        Write data to a JSON file.

        Args:
            data (T): The data to write to the JSON file.

        Raises:
            JSONDecodeError: If the data cannot be serialized to JSON.

        Returns:
            None

        """
        stored_data: FileData[T] = self.read()
        stored_data.metadata.version = self.metadata["version"]
        stored_data.metadata.title = self.metadata["title"]
        stored_data.metadata.description = self.metadata["description"]
        stored_data.metadata.timestamps = self.update_timestamps(
            stored_data.metadata.timestamps
        )
        stored_data.records = {**stored_data.records, **data}

        # Convert pydantic model to json string
        json_data: str = stored_data.model_dump_json(indent=2)

        # Write Json string to stored file.
        self.file_path.write_text(f"{json_data}\n")

    def update_timestamps(self, timestamps: Timestamp | None) -> Timestamp:
        """Return updated timestamp"""
        created_at: datetime = (
            now_utc() if timestamps is None else timestamps.created_at
        )

        return Timestamp(
            created_at=created_at,
            updated_at=now_utc(),
        )

    def delete(self) -> None:
        """
        Delete Created JSON file.

        Raises:
            PermissionError: Rise if you don't have permission to delete the file.

        Returns:
            None

        """
        if self.exists() and self.file_path.is_file():
            self.file_path.unlink()
