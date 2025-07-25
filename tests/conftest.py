from pytest import fixture, skip

from pydantic_storage._services import FileManager, FileStorage
from tests.mocks.models import FakeUser


# Fixture to create a FileManager instance
# --------------------------------------------
@fixture(scope="module")
def manager() -> FileManager[FakeUser]:
    return FileManager[FakeUser](
        file_path="./users.json",
        model_class=FakeUser,
        metadata={
            "version": "1.0.0",
            "title": "User records",
            "description": "User record descriptions",
        },
    )


@fixture(scope="module")
def storage() -> FileStorage[FakeUser]:
    skip(reason="Skipping test for FileStorage")
    return FileStorage[FakeUser](
        file_path="./users.json",
        model_class=FakeUser,
        metadata={
            "version": "1.0.0",
            "title": "User records",
            "description": "User record descriptions",
        },
        unique_fields=["id", "email"],
    )
