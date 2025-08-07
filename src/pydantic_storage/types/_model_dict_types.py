from datetime import datetime
from typing import Generic, NotRequired, TypedDict

from ._generic_types import T


class TimestampDict(TypedDict):
    created_at: NotRequired[datetime]
    updated_at: NotRequired[datetime]


class StorageDict(TypedDict):
    type: str
    format: str
    encryption: str


class BaseMetaDataDict(TypedDict):
    version: str
    title: str
    description: str


class FileMetaDataDict(BaseMetaDataDict):
    storage: StorageDict
    timestamps: NotRequired[TimestampDict]


class FileDataDict(TypedDict, Generic[T]):
    metadata: FileMetaDataDict
    records: list[T]
