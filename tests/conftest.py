from pytest import fixture

from pydantic_storage._services import FileManager, FileStorage
from tests.mocks.models import FakeUser


# Fixture to create a FileManager instance
# --------------------------------------------
@fixture(scope="module")
def manager() -> FileManager[FakeUser]:
    return FileManager[FakeUser](
        uri="tests/db/users.json",
        model=FakeUser,
        metadata={
            "version": "1.0.0",
            "title": "User records",
            "description": "User record descriptions",
        },
    )


@fixture(scope="module")
def file_storage() -> FileStorage[FakeUser]:
    return FileStorage(
        uri="tests/db/users.json",
        model=FakeUser,
        metadata={
            "version": "1.0.0",
            "title": "User records",
            "description": "User record descriptions",
        },
        unique_fields=["id", "email"],
    )
