from pytest import fixture, skip

from pydantic_storage._services import BaseFileManager, BaseFileStorage

from .test_helpers import FakeUser


# Fixture to create a BaseFileManager instance
# --------------------------------------------
@fixture(scope="module")
def manager() -> BaseFileManager[FakeUser]:
    return BaseFileManager[FakeUser](
        file_path="./users.json",
        model_class=FakeUser,
        metadata={
            "version": "1.0.0",
            "title": "User records",
            "description": "User record descriptions",
        },
    )


@fixture(scope="module")
def storage() -> BaseFileStorage[FakeUser]:
    skip(reason="Skipping test for BaseFileStorage")
    return BaseFileStorage[FakeUser](
        file_path="./users.json",
        model_class=FakeUser,
        metadata={
            "version": "1.0.0",
            "title": "User records",
            "description": "User record descriptions",
        },
        unique_fields=["id", "email"],
    )
