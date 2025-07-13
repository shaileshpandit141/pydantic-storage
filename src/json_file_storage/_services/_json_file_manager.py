from pathlib import Path
from pydantic import ValidationError as PydanticValidationError

from json_file_storage._abstractions._abstract_file_manager import AbstractFileManager
from json_file_storage.exceptions import ValidationError
from json_file_storage.models.typed import T, RecordsDict
from json_file_storage.models.pydantic import FileData


class JsonFileManager(AbstractFileManager[T]):
    """A class for managing JSON file operations."""

    def __init__(
        self,
        file_path: str,
        model_class: type[T],
        data: FileData[T],
    ) -> None:
        """Call parent initializer"""
        super().__init__(file_path, model_class, data)

        # Create file if user create instance of self class and add initial data.
        if not self.exists():
            self.create()

            # Convert pydantic model to json string
            json_data: str = self.data.model_dump_json(indent=2)

            # Write Json string to stored file.
            self.file.write_text(json_data)

    def exists(self) -> bool:
        """
        Check if the JSON file exists.

        Returns:
            bool: True if the file exists, False otherwise.

        """
        return self.file.exists()

    def create(self) -> None:
        """
        Create a new JSON file if it does not exist.

        Returns:
            None

        """
        # Check if the file already exists or not
        if not self.exists():
            # Create parent directories if they don't exist
            if self.file.parent != Path():
                self.file.parent.mkdir(parents=True, exist_ok=True)

            # Create the file (or update timestamp if it exists)
            self.file.touch(exist_ok=True)

    def read(self) -> FileData[T]:
        """
        Read data from a JSON file and return it.

        Returns:
            FileDict[T]: The data read from the JSON file.

        """
        try:
            file_data_text: str = self.file.read_text(encoding="utf-8")
            return FileData[T].model_validate_json(file_data_text)
        except PydanticValidationError as error:
            raise ValidationError(error) from error

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
        stored_data.metadata.version = self.data.metadata.version
        stored_data.metadata.title = self.data.metadata.title
        stored_data.metadata.description = self.data.metadata.description
        stored_data.metadata.storage = self.data.metadata.storage
        stored_data.metadata.timestamps = self.data.metadata.timestamps
        stored_data.records = {**stored_data.records, **self.data.records}

        # Convert pydantic model to json string
        json_data: str = stored_data.model_dump_json(indent=2)

        # Write Json string to stored file.
        self.file.write_text(json_data)

    def delete(self) -> None:
        """
        Delete Created JSON file.

        Raises:
            PermissionError: Rise if you don't have permission to delete the file.

        Returns:
            None

        """
        if self.exists() and self.file.is_file():
            self.file.unlink()
