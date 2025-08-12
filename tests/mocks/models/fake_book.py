from pydantic import BaseModel

from pydantic_storage.types import AutoID


class FakeBook(BaseModel):
    id: AutoID = 0
    title: str
    author: str
    published_year: int
