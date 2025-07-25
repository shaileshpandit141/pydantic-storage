from pathlib import Path


from pydantic_storage._services import BaseFileStorage

from .test_helpers import FakeUser


def test_json_file_storage_initialization(storage: BaseFileStorage[FakeUser]) -> None:
    """Test the initialization of BaseFileStorage."""
    assert isinstance(storage.file_path, Path)
    assert isinstance(storage.model_class, FakeUser)
    assert isinstance(storage.unique_fields, list)
