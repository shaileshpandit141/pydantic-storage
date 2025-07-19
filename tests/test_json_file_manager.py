from src.json_file_storage._services._json_file_manager import JsonFileManager
from pydantic import BaseModel
import pytest as pyt
from src.json_file_storage.models.pydantic import FileData


# ====================
# JSONFILEMANAGER TEST
# ====================


# DUMMY PYDANTIC MODELS
# ---------------------
class User(BaseModel):
    id: int
    name: str


@pyt.fixture
def manager() -> JsonFileManager[User]:
    return JsonFileManager[User](
        file_path="./users.json",
        model_class=User,
        metadata={
            "version": "1.0.0",
            "title": "User records",
            "description": "User record descriptions",
        },
    )


def test_json_file_manager_instance_created(
    manager: JsonFileManager[User],
) -> None:
    """Testing json file manager instance creation"""
    assert isinstance(manager, JsonFileManager)


def test_read_method(
    manager: JsonFileManager[User],
) -> None:
    """Testing read method"""
    data: FileData[User] = manager.read()

    # Check present records
    assert isinstance(data.metadata.version, str)
    assert isinstance(data.metadata.title, str)
    assert isinstance(data.metadata.description, str)
    assert isinstance(data.records, dict)


def test_write_and_read_users(
    manager: JsonFileManager[User],
) -> None:
    """Testing write method"""
    users: dict[int, User] = {
        1: User(id=1, name="Alice"),
        2: User(id=2, name="Bob"),
        3: User(id=3, name="Charlie"),
    }

    # Write all records to json file
    manager.write(users)

    # Read all record from json file
    data: FileData[User] = manager.read()

    # Check all records are present
    assert len(data.records) == 3
    assert data.records[1].name == "Alice"
    assert data.records[2].name == "Bob"
    assert data.records[3].name == "Charlie"
