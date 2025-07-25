from pathlib import Path

from pytest import mark

from pydantic_storage import BaseFileStorage

from .test_helpers import FakeUser

@mark.skip(reason="Not implemented yet")
def test_json_file_storage_initialization(storage: BaseFileStorage[FakeUser]) -> None:
    """Test the initialization of BaseFileStorage."""
    assert isinstance(storage.file_path, Path)
    assert isinstance(storage.model_class, FakeUser)
    assert isinstance(storage.unique_fields, list)
