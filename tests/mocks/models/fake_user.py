from pydantic import BaseModel


class FakeUser(BaseModel):
    id: int
    name: str
    email: str
