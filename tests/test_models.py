from datetime import datetime, timezone

from pydantic import BaseModel

from src.json_file_storage.models.pydantic import (
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
