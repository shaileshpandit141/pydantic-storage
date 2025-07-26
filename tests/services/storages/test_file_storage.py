from pathlib import Path

from pydantic import ValidationError
from pytest import raises

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


def test_get_method(storage: FileStorage[FakeUser]) -> None:
    """Test the get method of FileStorage."""
    user = storage.get(name="John Doe")
    assert isinstance(user, FakeUser)
    assert user.name == "John Doe"

    # Test with multiple key-value pair
    user = storage.get(
        name="Alice",
        email="alice@gmail.com",
    )
    assert isinstance(user, FakeUser)

    # Test with non-existing multiple key-value pair
    user = storage.get(
        name="Alice",
        email="shailesh@gmail.com",
    )
    assert isinstance(user, FakeUser)

    # Test with non-existing key-value pair
    user = storage.get(name="Non Existent")
    assert user is None

    # Test with invalid field
    with raises(ValidationError):
        storage.get(age=25)
