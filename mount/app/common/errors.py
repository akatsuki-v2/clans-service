from enum import Enum


class ServiceError(str, Enum):
    CLANS_CANNOT_CREATE = 'clans.cannot_create'
    CLANS_NOT_FOUND = 'clans.not_found'
    CLANS_ALREADY_IN_CLAN = 'clans.already_in_clan'
    CLANS_NAME_EXISTS = 'clans.name_exists'
    CLANS_TAG_EXISTS = 'clans.tag_exists'
