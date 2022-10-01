from enum import Enum
from typing import Any, Mapping, TypeVar

from pydantic import BaseModel as _pydantic_BaseModel


class Status(str, Enum):
    ACTIVE = 'active'
    DEACTIVATED = 'deactivated'
    DELETED = 'deleted'


T = TypeVar('T', bound=type['BaseModel'])


class BaseModel(_pydantic_BaseModel):
    class Config:
        anystr_strip_whitespace = True

    @classmethod
    def from_mapping(cls: T, mapping: Mapping[str, Any]) -> T:
        return cls(**{k: mapping[k] for k in cls.__fields__})
