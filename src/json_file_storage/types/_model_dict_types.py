from datetime import datetime
from typing import Generic, NotRequired, TypeAlias, TypedDict

from ._generic_types import T


class TimestampDict(TypedDict):
    created_at: NotRequired[datetime]
    updated_at: NotRequired[datetime]


class StorageDict(TypedDict):
    type: str
    encryption: str


class BaseMetaDataDict(TypedDict):
    version: str
    title: str
    description: str


class FileMetaDataDict(BaseMetaDataDict):
    storage: StorageDict
    timestamps: NotRequired[TimestampDict]


RecordsDict: TypeAlias = dict[int, T]


class FileDataDict(TypedDict, Generic[T]):
    metadata: FileMetaDataDict
    records: RecordsDict[T]
