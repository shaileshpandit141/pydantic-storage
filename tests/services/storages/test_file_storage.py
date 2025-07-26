from pathlib import Path

from pydantic_storage._services import FileStorage
from tests.mocks.models import FakeUser


def test_json_file_storage_initialization(storage: FileStorage[FakeUser]) -> None:
    """Test the initialization of FileStorage."""
    assert isinstance(storage.file_path, Path)
    assert isinstance(storage.model_class, FakeUser)
    assert isinstance(storage.unique_fields, list)


def test_all_method(storage: FileStorage[FakeUser]) -> None:
    """Test the all method of FileStorage."""
    items = storage.all()
    assert isinstance(items, list)
    assert all(isinstance(item, FakeUser) for item in items)
