from datetime import datetime
from typing import Generic

from pydantic import BaseModel, Field

from pydantic_storage.core import get_utc_time_now

from ..types import T


class Timestamp(BaseModel):
    created_at: datetime = Field(
        default_factory=get_utc_time_now,
        description="Creation timestamp (UTC)",
    )
    accessed_at: datetime = Field(
        default_factory=get_utc_time_now,
        description="Last accessed timestamp (UTC)",
    )
    modified_at: datetime = Field(
        default_factory=get_utc_time_now,
        description="Last modified timestamp (UTC)",
    )


class Storage(BaseModel):
    uri: str = Field(
        ..., description="Storage backend location (e.g., /db/records.json)"
    )
    backend: str = Field(..., description="Storage backend type (e.g., local, s3, ...)")
    format: str = Field(
        ..., description="Storage backend format (e.g., json, yml, ...)"
    )
    encryption: str = Field(..., description="Encryption method used (e.g., AES256)")


class MetaData(BaseModel):
    version: str = Field(
        default="1.0.0",
        description="Schema or file version",
        pattern=r"^\d+\.\d+\.\d+(-[a-zA-Z0-9.]+)?(\+[a-zA-Z0-9.]+)?$",
    )
    title: str = Field(..., description="Human-readable title of the file")
    description: str = Field(..., description="Brief description of the file contents")
    storage: Storage | None = None
    timestamps: Timestamp = Timestamp()


class Data(BaseModel, Generic[T]):
    metadata: MetaData
    records: list[T] = Field(
        default_factory=list[T],
        description="Keyed collection of typed records",
    )
