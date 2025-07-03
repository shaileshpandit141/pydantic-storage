from typing import Any, TypedDict, TypeVar

from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


class TimestampDict(TypedDict):
    created_at: str
    updated_at: str


class StorageDict(TypedDict):
    type: str
    encryption: str


class MetaDataConfigDict(TypedDict):
    version: str
    title: str
    description: str


class MetaDataDict(MetaDataConfigDict):
    storage: StorageDict
    timestamps: TimestampDict


class JsonFileDict(TypedDict):
    metadata: MetaDataDict
    records: dict[str, Any]
