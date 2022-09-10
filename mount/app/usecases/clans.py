from typing import Any, Mapping

from app.common.context import Context
from app.common.errors import ServiceError
from app.models.clans import JoinMethod
from app.repositories.clans import ClansRepo


async def create(ctx: Context,
                 name: str,
                 tag: str,
                 description: str,
                 owner: int,
                 join_method: JoinMethod) -> Mapping[str, Any] | ServiceError:
    repo = ClansRepo(ctx)

    if await repo.fetch_one(owner=owner):
        return ServiceError.CLANS_ALREADY_IN_CLAN

    if await repo.fetch_one(name=name):
        return ServiceError.CLANS_NAME_EXISTS

    if await repo.fetch_one(tag=tag):
        return ServiceError.CLANS_TAG_EXISTS

    clan = await repo.create(name, tag, description, owner, join_method)
    return clan


async def fetch_one(ctx: Context, clan_id: int) -> Mapping[str, Any] | ServiceError:
    repo = ClansRepo(ctx)
    clan = await repo.fetch_one(clan_id=clan_id)
    if not clan:
        return ServiceError.CLANS_NOT_FOUND

    return clan


async def fetch_all(ctx: Context) -> list[Mapping[str, Any]]:
    repo = ClansRepo(ctx)
    clans = await repo.fetch_all()
    return clans


async def partial_update(ctx: Context,
                         clan_id: int,
                         **kwargs: Any | None) -> Mapping[str, Any] | ServiceError:
    repo = ClansRepo(ctx)

    clan = await repo.fetch_one(clan_id=clan_id)
    if not clan:
        return ServiceError.CLANS_NOT_FOUND

    if not kwargs:
        return clan

    new_tag = kwargs.get("tag")
    new_name = kwargs.get("name")

    if new_tag and await repo.fetch_one(tag=new_tag):
        return ServiceError.CLANS_TAG_EXISTS

    if new_name and await repo.fetch_one(name=new_name):
        return ServiceError.CLANS_NAME_EXISTS

    clan = await repo.partial_update(clan_id, **kwargs)
    return clan
