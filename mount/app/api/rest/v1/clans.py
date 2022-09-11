from fastapi import APIRouter, Depends

from app.api.rest.context import RequestContext
from app.common import responses
from app.common.errors import ServiceError
from app.models.clans import Clan, CreateClan, UpdateClan
from app.usecases import clans

router = APIRouter(tags=["Clans"])


# https://osuakatsuki.atlassian.net/browse/V2-20
@router.post("/clans", response_model=Clan)
async def create_clan(args: CreateClan, ctx: RequestContext = Depends()):
    data = await clans.create(ctx,
                              args.name,
                              args.tag,
                              args.description,
                              args.owner,
                              args.join_method)
    if isinstance(data, ServiceError):
        return responses.failure(data, "Failed to create clan")

    resp = Clan.from_mapping(data)
    return responses.success(resp)

# https://osuakatsuki.atlassian.net/browse/V2-21
@router.get("/clans/{clan_id}", response_model=Clan)
async def get_clan(clan_id: int, ctx: RequestContext = Depends()):
    data = await clans.fetch_one(ctx, clan_id)
    if isinstance(data, ServiceError):
        return responses.failure(data, "Failed to get clan")

    resp = Clan.from_mapping(data)
    return responses.success(resp)

@router.get("/clans", response_model=Clan)
async def get_clans(ctx: RequestContext = Depends()):
    data = await clans.fetch_all(ctx)
    resp = [Clan.from_mapping(clan) for clan in data]
    return responses.success(resp)

# https://osuakatsuki.atlassian.net/browse/V2-64
@router.patch("/clans/{clan_id}", response_model=Clan)
async def partial_update_clan(clan_id: int, args: UpdateClan,
                              ctx: RequestContext = Depends()):
    data = await clans.partial_update(ctx, clan_id, **args.dict())
    if isinstance(data, ServiceError):
        return responses.failure(data, "Failed to update clan")

    resp = Clan.from_mapping(data)
    return responses.success(resp)

# https://osuakatsuki.atlassian.net/browse/V2-23
@router.delete("/clans/{clan_id}", response_model=Clan)
async def disband_clan(clan_id: int, ctx: RequestContext = Depends()):
    data = await clans.disband(ctx, clan_id)
    if isinstance(data, ServiceError):
        return responses.failure(data, "Failed to disband clan")

    resp = Clan.from_mapping(data)
    return responses.success(resp)