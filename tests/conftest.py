from pytest import fixture
from pydantic import BaseModel

from json_file_storage._services import JsonFileManager, JsonFileStorage
from .test_helpers import FakeUser


# Dummy User model for testing
# ----------------------------
class User(BaseModel):
    id: int
    name: str


# Fixture to create a JsonFileManager instance
# --------------------------------------------
@fixture(scope="module")
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


@fixture(scope="module")
def storage() -> JsonFileStorage[FakeUser]:
    return JsonFileStorage[FakeUser](
        file_path="./users.json",
        model_class=User,
        metadata={
            "version": "1.0.0",
            "title": "User records",
            "description": "User record descriptions",
        },
        unique_fields=["id", "email"],
    )
