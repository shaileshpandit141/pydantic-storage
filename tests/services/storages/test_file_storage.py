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


def test_get_data(
    file_storage: FileStorage[FakeUser],
) -> None:
    """Test get a single item from file"""
    data1 = file_storage.get(id=2)
    data2 = file_storage.get(id=2, email="fake@gmail.co.com")

    if data1:
        assert data1.id == 2

    assert data2 is None


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


def test_count_all_data(
    file_storage: FileStorage[FakeUser],
) -> None:
    """Test to count all data"""
    count = file_storage.count()

    assert count > 0


def test_exists_data(
    file_storage: FileStorage[FakeUser],
) -> None:
    """Test to chaeck a data is exists or not"""
    exists = file_storage.exists(email="shailesh@gmail.com")
    assert exists is True


def test_filter_data(
    file_storage: FileStorage[FakeUser],
) -> None:
    """Test get all data from file"""
    filter_data1 = file_storage.filter(
        name="nice",
        email="nice@gmail.com",
    )

    filter_data2 = file_storage.filter(
        id=2,
        name="nice",
    )

    assert filter_data1[0].email == "nice@gmail.com"
    assert len(filter_data2) == 0


def test_delete_data(
    file_storage: FileStorage[FakeUser],
) -> None:
    """Test get all data from file"""
    deleted_data = file_storage.delete(id=6)

    assert deleted_data.id == 6  # type: ignore
    assert deleted_data.name == "ashis"  # type: ignore
    assert deleted_data.email == "ashis@gmail.com"  # type: ignore
