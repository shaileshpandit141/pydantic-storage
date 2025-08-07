from datetime import datetime, timezone
from typing import Any, ClassVar, Generic

from pydantic import BaseModel, ConfigDict, Field, model_validator

from ..types import T


def now_utc() -> datetime:
    return datetime.now(timezone.utc)


class Timestamp(BaseModel):
    created_at: datetime = Field(
        default_factory=now_utc,
        description="Creation timestamp (UTC)",
    )
    updated_at: datetime = Field(
        default_factory=now_utc,
        description="Last update timestamp (UTC)",
    )

    @model_validator(mode="before")
    @classmethod
    def update_timestamp(cls, values: dict[str, Any]) -> dict[str, Any]:
        now: datetime = now_utc()
        if "created_at" not in values:
            values["created_at"] = now
        values["updated_at"] = now
        return values


class Storage(BaseModel):
    type: str = Field(..., description="Storage backend type (e.g., local, s3, ...)")
    format: str = Field(
        ..., description="Storage backend format (e.g., json, yml, ...)"
    )
    encryption: str = Field(..., description="Encryption method used (e.g., AES256)")


class BaseMetaData(BaseModel):
    version: str = Field(
        default="1.0.0",
        description="Schema or file version",
        pattern=r"^\d+\.\d+\.\d+(-[a-zA-Z0-9.]+)?(\+[a-zA-Z0-9.]+)?$",
    )
    title: str = Field(..., description="Human-readable title of the file")
    description: str = Field(..., description="Brief description of the file contents")


class FileMetaData(BaseMetaData):
    storage: Storage
    timestamps: Timestamp | None = None


class FileData(BaseModel, Generic[T]):
    metadata: FileMetaData
    records: dict[int, T] = Field(
        default_factory=dict[int, T],
        description="Keyed collection of typed records",
    )

    model_config = ConfigDict(extra="forbid")

    json_schema_extra: ClassVar = {
        "examples": [
            {
                "metadata": {
                    "version": "1.0",
                    "title": "Example File",
                    "description": "Sample metadata",
                    "storage": {"type": "s3", "encryption": "AES256"},
                    "timestamps": {
                        "created_at": "2025-01-01T00:00:00Z",
                        "updated_at": "2025-07-01T00:00:00Z",
                    },
                },
                "records": {1: {"id": 1, "name": "Alice"}},
            }
        ]
    }
