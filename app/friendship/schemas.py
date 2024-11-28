from typing import Optional

from pydantic import BaseModel, Field


class FriendshipEntitySchema(BaseModel):
    id: int
    type: str
    username: str
    first_name: Optional[str] = Field(default=None)
    last_name: Optional[str] = Field(default=None)


class NewFriendshipEntitySchema(BaseModel):
    username: str
