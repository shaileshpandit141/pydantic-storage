import json
from pathlib import Path

from json_file_storage._abstractions._abstract_file_manager import AbstractFileManager
from json_file_storage.exceptions import JSONDecodeError, JSONEncodeError
from json_file_storage.models.typed import FileDict, T


class JsonFileManager(AbstractFileManager[T]):
    """A class for managing JSON file operations."""

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

    def read(self) -> FileDict[T]:
        """
        Read data from a JSON file and return it.

        Returns:
            FileDict[T]: The data read from the JSON file.

        """
        try:
            return json.loads(self.file.read_text(encoding="utf-8"))
        except json.JSONDecodeError as error:
            raise JSONDecodeError(error) from error

    def write(self, data: FileDict[T]) -> None:
        """
        Write data to a JSON file.

        Args:
            data (T): The data to write to the JSON file.

        Raises:
            JSONDecodeError: If the data cannot be serialized to JSON.

        Returns:
            None

        """
        try:
            self.file.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
        except TypeError as error:
            raise JSONEncodeError(error) from error

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
