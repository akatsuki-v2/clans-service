from datetime import datetime
from enum import Enum

from pydantic import Field

from . import BaseModel


class JoinMethod(str, Enum):
    OPEN = 'open'
    BY_REQUEST = 'by-request'
    INVITE_ONLY = 'invite-only'
    CLOSED = 'closed'


#
# Input
#
class CreateClan(BaseModel):
    name: str = Field(..., min_length=1, max_length=32)
    tag: str = Field(..., min_length=1, max_length=8)
    description: str | None
    owner: int
    join_method: JoinMethod


class UpdateClan(BaseModel):
    name: str | None = Field(None, min_length=1, max_length=32)
    tag: str | None = Field(None, min_length=1, max_length=8)
    description: str | None
    owner: int | None
    join_method: JoinMethod | None


#
# Output
#
class Clan(BaseModel):
    clan_id: int
    name: str
    tag: str
    description: str | None
    owner: int
    created_at: datetime
    updated_at: datetime
