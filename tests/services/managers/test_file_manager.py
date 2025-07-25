from pydantic_storage._services import FileManager
from pydantic_storage.models import FileData

from tests.test_helpers import FakeUser

# ================
# Filemanager Test
# ================


def test_json_file_manager_instance_created(
    manager: FileManager[FakeUser],
) -> None:
    """Testing json file manager instance creation"""
    assert isinstance(manager, FileManager)


def test_read_method(
    manager: FileManager[FakeUser],
) -> None:
    """Testing read method"""
    data: FileData[FakeUser] = manager.read()

    # Check present records
    assert isinstance(data.metadata.version, str)
    assert isinstance(data.metadata.title, str)
    assert isinstance(data.metadata.description, str)
    assert isinstance(data.records, dict)


def test_write_and_read_users(
    manager: FileManager[FakeUser],
) -> None:
    """Testing write method"""
    users: dict[int, FakeUser] = {
        1: FakeUser(id=1, name="Alice", email="alice@gmail.com"),
        2: FakeUser(id=2, name="Bob", email="bob@gmail.com"),
        3: FakeUser(id=3, name="Charlie", email="charlie@gmail.com"),
    }

    # Write all records to json file
    manager.write(users)

    # Read all record from json file
    data: FileData[FakeUser] = manager.read()

    # Check all records are present
    assert len(data.records) == 3
    assert data.records[1].name == "Alice"
    assert data.records[2].name == "Bob"
    assert data.records[3].name == "Charlie"
