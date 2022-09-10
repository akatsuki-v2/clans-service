from enum import Enum


class ServiceError(str, Enum):
    CLANS_CANNOT_CREATE = 'clans.cannot_create'
    CLANS_NOT_FOUND = 'clans.not_found'
