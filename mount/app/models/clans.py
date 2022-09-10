from enum import Enum

class JoinMethod(str, Enum):
    OPEN = 'open'
    BY_REQUEST = 'by-request'
    INVITE_ONLY = 'invite-only'
