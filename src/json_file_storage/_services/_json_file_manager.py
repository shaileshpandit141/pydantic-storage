import json
from pathlib import Path

from json_file_storage._abstractions._abstract_file_manager import AbstractFileManager
from json_file_storage.exceptions import JSONDecodeError
from json_file_storage.models.typed import JsonFileDict, T


class JsonFileManager(AbstractFileManager[T]):
    """A class for managing JSON file operations."""

    def __init__(self, file_path: str) -> None:
        """Initialize the JsonFileManager."""
        self.file: Path = Path(file_path)

    def exists(self) -> bool:
        """
        Check if the JSON file exists.

        Returns:
            bool: True if the file exists, False otherwise.

        """
        return self.file.exists()

    def read(self) -> JsonFileDict[T]:
        """
        Read data from a JSON file and return it.

        Returns:
            JsonFileDict[T]: The data read from the JSON file.

        """
        try:
            return json.loads(self.file.read_text(encoding="utf-8"))
        except json.JSONDecodeError as error:
            raise JSONDecodeError(error) from error
