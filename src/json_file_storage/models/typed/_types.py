from typing import Generic, NotRequired, TypeAlias, TypedDict, TypeVar

from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


class TimestampDict(TypedDict):
    created_at: NotRequired[str]
    updated_at: NotRequired[str]


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


RecordDict: TypeAlias = dict[str, T]


class FileDataDict(TypedDict, Generic[T]):
    metadata: FileMetaDataDict
    records: RecordDict[T]
