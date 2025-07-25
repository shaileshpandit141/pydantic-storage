from pathlib import Path


from pydantic_storage._services import FileStorage

from .test_helpers import FakeUser


def test_json_file_storage_initialization(storage: FileStorage[FakeUser]) -> None:
    """Test the initialization of FileStorage."""
    assert isinstance(storage.file_path, Path)
    assert isinstance(storage.model_class, FakeUser)
    assert isinstance(storage.unique_fields, list)
