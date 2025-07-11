from datetime import datetime, timezone

import pytest
from pydantic import BaseModel, ValidationError

from src.json_file_storage.models.pydantic import (
    Storage,
    Timestamp,
)


# Dummy record model for generic T
class DummyRecord(BaseModel):
    id: int
    name: str


# === TIMESTAMP TESTS ===


def test_timestamp_defaults() -> None:
    ts = Timestamp()
    assert isinstance(ts.created_at, datetime)
    assert isinstance(ts.updated_at, datetime)
    assert ts.created_at.tzinfo == timezone.utc
    assert ts.updated_at.tzinfo == timezone.utc
    assert ts.updated_at >= ts.created_at


def test_timestamp_custom_created_at() -> None:
    custom_time = datetime(2020, 1, 1, tzinfo=timezone.utc)
    ts = Timestamp(created_at=custom_time)
    assert ts.created_at == custom_time
    assert ts.updated_at >= custom_time


# === STORAGE TESTS ===


def test_valid_storage() -> None:
    s = Storage(type="s3", encryption="AES256")
    assert s.type == "s3"
    assert s.encryption == "AES256"


def test_invalid_storage_missing_field() -> None:
    with pytest.raises(ValidationError):
        Storage(type="s3")  # type: ignore (missing encryption)
