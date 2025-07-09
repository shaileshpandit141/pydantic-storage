from typing import Generic, TypeAlias, TypedDict, TypeVar

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


RecordDict: TypeAlias = dict[str, T]


class FileDict(TypedDict, Generic[T]):
    metadata: MetaDataDict
    records: RecordDict[T]
