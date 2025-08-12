from pydantic_storage._services import FileStorage
from tests.mocks.models import FakeUser


def test_file_storage_instance(
    file_storage: FileStorage[FakeUser],
) -> None:
    """Test the instance of FileStorage."""
    assert isinstance(file_storage.uri, str)
    assert isinstance(file_storage.unique_fields, list)
    assert file_storage.model is FakeUser


def test_get_all_data(
    file_storage: FileStorage[FakeUser],
) -> None:
    """Test get all data from file"""
    assert isinstance(file_storage.all(), list)


def test_create_data(
    file_storage: FileStorage[FakeUser],
) -> None:
    """Test create data"""
    data: list[FakeUser] = [
        FakeUser(name="ashis", email="ashis@gmail.com"),
    ]
    created_data = file_storage.create(data=data)

    if len(created_data) > 0:
        assert data[0].name == created_data[0].name
