from pydantic import BaseModel

from pydantic_storage.types import AutoID


class FakeUser(BaseModel):
    id: AutoID = 0
    name: str
    email: str
