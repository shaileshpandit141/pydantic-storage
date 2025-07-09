from typing import ClassVar, Generic, TypeVar

from pydantic import BaseModel, Field

T = TypeVar("T", bound=BaseModel)


class Timestamp(BaseModel):
    created_at: str = Field(..., description="Creation timestamp (ISO 8601)")
    updated_at: str = Field(..., description="Last update timestamp (ISO 8601)")


class Storage(BaseModel):
    type: str = Field(..., description="Storage backend type (e.g., local, s3)")
    encryption: str = Field(..., description="Encryption method used (e.g., AES256)")


class BaseMetaData(BaseModel):
    version: str = Field(..., description="Schema or file version")
    title: str = Field(..., description="Human-readable title of the file")
    description: str = Field(..., description="Brief description of the file contents")


class FileMetaData(BaseMetaData):
    storage: Storage
    timestamps: Timestamp


class FileData(BaseModel, Generic[T]):
    metadata: FileMetaData
    records: dict[int, T] = Field(
        default_factory=dict,
        description="Keyed collection of typed records",
    )

    class Config:
        extra: str = "forbid"
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
