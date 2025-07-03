from typing import Any, TypedDict, TypeVar

from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


class TimestampDict(TypedDict):
    created_at: str
    updated_at: str


class StorageDict(TypedDict):
    type: str
    encryption: str


class MetaDataDict(TypedDict):
    version: str
    title: str
    description: str
    timestamps: TimestampDict
    storage: StorageDict
    records: dict[str, Any]
