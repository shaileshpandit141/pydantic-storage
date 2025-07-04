from pathlib import Path

from json_file_storage._abstractions._abstract_file_manager import AbstractFileManager
from json_file_storage.models.typed import T


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
