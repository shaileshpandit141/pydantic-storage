from src.json_file_storage._services._json_file_manager import JsonFileManager
from pydantic import BaseModel
import pytest as pyt


# =====================
# DUMMY PYDANTIC MODELS
# =====================


class User(BaseModel):
    id: int
    name: str


# ====================
# JSONFILEMANAGER TEST
# ====================


@pyt.fixture
def manager_instance() -> JsonFileManager[User]:
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
    manager_instance: JsonFileManager[User],
) -> None:
    """Testing json file manager instance creation"""
    assert isinstance(manager_instance, JsonFileManager)
