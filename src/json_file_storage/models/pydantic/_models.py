from typing import TypeVar

from pydantic import BaseModel, Field

T = TypeVar("T", bound=BaseModel)


class Timestamp(BaseModel):
    created_at: str = Field(..., description="Creation timestamp (ISO 8601)")
    updated_at: str = Field(..., description="Last update timestamp (ISO 8601)")
