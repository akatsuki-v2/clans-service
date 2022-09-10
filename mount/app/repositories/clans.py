from enum import Enum
from typing import Any, Mapping

from app.common.context import Context
from app.models import Status


class JoinMethod(str, Enum):
    OPEN = 'open'
    BY_REQUEST = 'by-request'
    INVITE_ONLY = 'invite-only'


class ClansRepo:
    READ_PARAMS = """\
        clan_id, name, tag, description,
        owner, join_method, status,
        created_at, updated_at
    """

    def __init__(self, ctx: Context) -> None:
        self.ctx = ctx

    async def create(self,
                     name: str,
                     tag: str,
                     description: str,
                     owner: int,
                     join_method: JoinMethod,
                     status: Status):
        query = f"""\
            INSERT INTO clans (name, tag, description, owner, join_method, status)
                VALUES (:name, :tag, :description, :owner, :join_method, :status)
              RETURNING {self.READ_PARAMS}
        """
        params = {
            "name": name,
            "tag": tag,
            "description": description,
            "owner": owner,
            "join_method": join_method,
            "status": status,
        }
        clans = await self.ctx.db.fetch_one(query, params)
        return clans

    async def fetch_one(self, clan_id: int | None = None,
                        tag: str | None = None, name: str | None = None,
                        status: Status | None = None) -> Mapping[str, Any] | None:
        query = f"""\
            SELECT {self.READ_PARAMS}
              FROM clans
            WHERE clan_id = COALESCE(:clan_id, clan_id)
                AND name = COALESCE(:name, name)
                AND tag = COALESCE(:tag, tag)
                AND status = COALESCE(:status, status)
        """
        params = {
            "clan_id": clan_id,
            "tag": tag,
            "name": name,
            "status": status,
        }
        clan = await self.ctx.db.fetch_one(query, params)
        return clan

    async def fetch(self, clan_id: int | None = None,
                    tag: str | None = None, name: str | None = None,
                    status: Status | None = None) -> list[Mapping[str, Any]]:
        query = f"""\
            SELECT {self.READ_PARAMS}
              FROM clans
            WHERE clan_id = COALESCE(:clan_id, clan_id)
                AND name = COALESCE(:name, name)
                AND tag = COALESCE(:tag, tag)
                AND status = COALESCE(:status, status)
        """
        params = {
            "clan_id": clan_id,
            "tag": tag,
            "name": name,
            "status": status,
        }
        clans = await self.ctx.db.fetch_all(query, params)
        return clans

    async def partial_update(self, clan_id: int, **updates) -> Mapping[str, Any] | None:
        query = f"""\
            UPDATE clans SET
                name = COALESCE(:name, name),
                tag = COALESCE(:tag, tag),
                description = COALESCE(:description, description),
                owner = COALESCE(:owner, owner),
                join_method = COALESCE(:join_method, join_method),
                status = COALESCE(:status, status),
                updated_at = CURRENT_TIMESTAMP,
              WHERE clan_id = :clan_id
            RETURNING {self.READ_PARAMS}
        """
        params = {
            "clan_id": clan_id,
            "tag": None,
            "name": None,
            "description": None,
            "owner": None,
            "join_method": None,
            "status": None,
        } | updates
        clan = await self.ctx.db.fetch_one(query, params)
        return clan
