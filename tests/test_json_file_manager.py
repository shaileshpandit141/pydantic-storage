from src.json_file_storage._services._json_file_manager import JsonFileManager
from pydantic import BaseModel


# =====================
# DUMMY PYDANTIC MODELS
# =====================


class User(BaseModel):
    id: int
    name: str


# ====================
# JSONFILEMANAGER TEST
# ====================


def initilize_json_file_manager() -> JsonFileManager[User]:
    return JsonFileManager[User](
        file_path="./users.json",
        model_class=User,
        metadata={
            "version": "1.0.0",
            "title": "User records",
            "description": "User record descriptions",
        },
    )


def test_create_json_file_manager_instance() -> None:
    """Testing json file manager instance creation"""
    manager: JsonFileManager[User] = initilize_json_file_manager()

    assert isinstance(manager, JsonFileManager)
