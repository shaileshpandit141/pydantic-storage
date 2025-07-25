from pathlib import Path

from pydantic_storage import JsonFileStorage

from .test_helpers import FakeUser


def test_json_file_storage_initialization(storage: JsonFileStorage[FakeUser]) -> None:
    """Test the initialization of JsonFileStorage."""
    assert isinstance(storage.file_path, Path)
    assert isinstance(storage.model_class, FakeUser)
    assert isinstance(storage.unique_fields, list)
