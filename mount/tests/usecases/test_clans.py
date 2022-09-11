import pytest
from app.common.context import Context
from app.common.errors import ServiceError
from app.models.clans import JoinMethod
from app.usecases import clans

# https://docs.pytest.org/en/7.1.x/reference/reference.html#globalvar-pytestmark
pytestmark = pytest.mark.asyncio


async def test_should_pass(ctx: Context):
    assert ctx is not None


async def test_should_create(ctx: Context):
    name = "Akatsuki Quality Control"
    tag = "AQC"
    description = "The"
    owner = 1000
    join_method = JoinMethod.CLOSED

    data = await clans.create(ctx, name, tag, description, owner, join_method)
    assert not isinstance(data, ServiceError)

    assert data["clan_id"] is not None
    assert data["name"] == name
    assert data["tag"] == tag
    assert data["description"] == description
    assert data["owner"] == owner
    assert data["join_method"] == join_method
    assert data["created_at"] is not None
    assert data["updated_at"] is not None


async def test_should_fail_already_in_clan(ctx: Context):
    name = "Akatsuki Buality Control"
    tag = "ABC"
    description = "The"
    owner = 1935
    join_method = JoinMethod.CLOSED

    data = await clans.create(ctx, name, tag, description, owner, join_method)
    assert not isinstance(data, ServiceError)

    assert data["clan_id"] is not None
    assert data["name"] == name
    assert data["tag"] == tag
    assert data["description"] == description
    assert data["owner"] == owner
    assert data["join_method"] == join_method
    assert data["created_at"] is not None
    assert data["updated_at"] is not None

    name = "Akatsuki Quality Control 2"
    tag = "AQC2"
    description = "The"
    owner = 1935
    join_method = JoinMethod.CLOSED

    data = await clans.create(ctx, name, tag, description, owner, join_method)
    assert isinstance(data, ServiceError)
    assert data == ServiceError.CLANS_ALREADY_IN_CLAN


async def test_should_fail_existing_tag(ctx: Context):
    name = "Bkatsuki Quality Control"
    tag = "BQC"
    description = "The"
    owner = 1936
    join_method = JoinMethod.CLOSED

    data = await clans.create(ctx, name, tag, description, owner, join_method)
    assert not isinstance(data, ServiceError)

    assert data["clan_id"] is not None
    assert data["name"] == name
    assert data["tag"] == tag
    assert data["description"] == description
    assert data["owner"] == owner
    assert data["join_method"] == join_method
    assert data["created_at"] is not None
    assert data["updated_at"] is not None

    name = "Bkatsuki Quality Control 2"
    tag = "BQC"
    description = "The"
    owner = 1001
    join_method = JoinMethod.CLOSED

    data = await clans.create(ctx, name, tag, description, owner, join_method)
    assert isinstance(data, ServiceError)
    assert data == ServiceError.CLANS_TAG_EXISTS


async def test_should_fail_existing_name(ctx: Context):
    name = "Dkatsuki Quality Control"
    tag = "DQC"
    description = "The"
    owner = 1938
    join_method = JoinMethod.CLOSED

    data = await clans.create(ctx, name, tag, description, owner, join_method)
    assert not isinstance(data, ServiceError)

    assert data["clan_id"] is not None
    assert data["name"] == name
    assert data["tag"] == tag
    assert data["description"] == description
    assert data["owner"] == owner
    assert data["join_method"] == join_method
    assert data["created_at"] is not None
    assert data["updated_at"] is not None

    name = "Dkatsuki Quality Control"
    tag = "DQC2"
    description = "The"
    owner = 1002
    join_method = JoinMethod.CLOSED

    data = await clans.create(ctx, name, tag, description, owner, join_method)
    assert isinstance(data, ServiceError)
    assert data == ServiceError.CLANS_NAME_EXISTS


async def test_should_fetch_one(ctx: Context):
    name = "Fkatsuki Quality Control"
    tag = "FQC"
    description = "The"
    owner = 1939
    join_method = JoinMethod.CLOSED

    data = await clans.create(ctx, name, tag, description, owner, join_method)
    assert not isinstance(data, ServiceError)

    assert data["clan_id"] is not None
    clan_id = data["clan_id"]

    data = await clans.fetch_one(ctx, clan_id)
    assert not isinstance(data, ServiceError)

    assert data["clan_id"] == clan_id
    assert data["name"] == name
    assert data["tag"] == tag
    assert data["description"] == description
    assert data["owner"] == owner
    assert data["join_method"] == join_method
    assert data["created_at"] is not None
    assert data["updated_at"] is not None


async def test_should_fail_fetch_one_no_clan(ctx: Context):
    data = await clans.fetch_one(ctx, 0)
    assert isinstance(data, ServiceError)
    assert data == ServiceError.CLANS_NOT_FOUND


async def test_should_fetch_all(ctx: Context):
    data = await clans.fetch_all(ctx)
    assert not isinstance(data, ServiceError)


async def test_should_partial_update(ctx: Context):
    name = "Hkatsuki Quality Control"
    tag = "HQC"
    description = "The"
    owner = 1940
    join_method = JoinMethod.CLOSED

    data = await clans.create(ctx,name, tag, description, owner, join_method)
    assert not isinstance(data, ServiceError)

    assert data["clan_id"] is not None
    clan_id = data["clan_id"]

    assert data["name"] == name
    assert data["tag"] == tag
    assert data["description"] == description
    assert data["owner"] == owner
    assert data["join_method"] == join_method
    assert data["created_at"] is not None
    assert data["updated_at"] is not None

    new_name = "Hkatsuki Quality Control 2"
    new_tag = "HHC"
    new_description = "The new control"
    new_owner = 1040
    new_join_method = JoinMethod.INVITE_ONLY

    data = await clans.partial_update(ctx,
                                      clan_id,
                                      name=new_name,
                                      tag=new_tag,
                                      description=new_description,
                                      owner=new_owner,
                                      join_method=new_join_method)
    assert not isinstance(data, ServiceError)
    
    assert data["clan_id"] is not None
    assert data["name"] == new_name
    assert data["tag"] == new_tag
    assert data["description"] == new_description
    assert data["owner"] == new_owner
    assert data["join_method"] == new_join_method
    assert data["created_at"] is not None
    assert data["updated_at"] is not None


async def test_should_fail_partial_update_no_change(ctx: Context):
    name = "Haakatsuki Quality Control"
    tag = "HQCa"
    description = "The"
    owner = 1940
    join_method = JoinMethod.CLOSED

    data = await clans.create(ctx,name, tag, description, owner, join_method)
    assert not isinstance(data, ServiceError)

    assert data["clan_id"] is not None
    clan_id = data["clan_id"]

    assert data["name"] == name
    assert data["tag"] == tag
    assert data["description"] == description
    assert data["owner"] == owner
    assert data["join_method"] == join_method
    assert data["created_at"] is not None
    assert data["updated_at"] is not None

    data = await clans.partial_update(ctx, clan_id)
    assert not isinstance(data, ServiceError)
    
    assert data["clan_id"] is not None
    assert data["name"] == name
    assert data["tag"] == tag
    assert data["description"] == description
    assert data["owner"] == owner
    assert data["join_method"] == join_method
    assert data["created_at"] is not None
    assert data["updated_at"] is not None


async def test_should_fail_partial_update_no_clan(ctx: Context):
    new_name = "Gkatsuki 2"
    data = await clans.partial_update(ctx, 0, name=new_name)
    assert isinstance(data, ServiceError)
    assert data == ServiceError.CLANS_NOT_FOUND


async def test_should_fail_partial_update_name_exists(ctx: Context):
    first_name = "Gkatsuki Quality Control"
    tag = "GQC"
    description = "The"
    owner = 19234
    join_method = JoinMethod.CLOSED

    data = await clans.create(ctx, first_name, tag, description, owner, join_method)
    assert not isinstance(data, ServiceError)

    assert data["clan_id"] is not None
    assert data["name"] == first_name
    assert data["tag"] == tag
    assert data["description"] == description
    assert data["owner"] == owner
    assert data["join_method"] == join_method
    assert data["created_at"] is not None
    assert data["updated_at"] is not None


    # 2nd clan
    name = "QWkatsuki Quality Control 2"
    tag = "QWQC2"
    description = "The"
    owner = 100123
    join_method = JoinMethod.CLOSED

    data = await clans.create(ctx, name, tag, description, owner, join_method)
    assert not isinstance(data, ServiceError)

    assert data["clan_id"] is not None
    clan_id = data["clan_id"]

    assert data["name"] == name
    assert data["tag"] == tag
    assert data["description"] == description
    assert data["owner"] == owner
    assert data["join_method"] == join_method
    assert data["created_at"] is not None
    assert data["updated_at"] is not None

    # 2nd clan name update
    data = await clans.partial_update(ctx, clan_id, name=first_name)
    assert isinstance(data, ServiceError)
    assert data == ServiceError.CLANS_NAME_EXISTS


async def test_should_fail_partial_update_tag_exists(ctx: Context):
    name = "AAAAAAAkatsuki Quality Control"
    first_tag = "AAAAQC"
    description = "The"
    owner = 135
    join_method = JoinMethod.CLOSED

    data = await clans.create(ctx, name, first_tag, description, owner, join_method)
    assert not isinstance(data, ServiceError)

    assert data["clan_id"] is not None
    assert data["name"] == name
    assert data["tag"] == first_tag
    assert data["description"] == description
    assert data["owner"] == owner
    assert data["join_method"] == join_method
    assert data["created_at"] is not None
    assert data["updated_at"] is not None


    # 2nd clan
    name = "Aegrgekatsuki Quality C"
    tag = "AQCgh2"
    description = "The"
    owner = 101
    join_method = JoinMethod.CLOSED

    data = await clans.create(ctx, name, tag, description, owner, join_method)
    assert not isinstance(data, ServiceError)

    assert data["clan_id"] is not None
    clan_id = data["clan_id"]

    assert data["name"] == name
    assert data["tag"] == tag
    assert data["description"] == description
    assert data["owner"] == owner
    assert data["join_method"] == join_method
    assert data["created_at"] is not None
    assert data["updated_at"] is not None

    # 2nd clan name update
    data = await clans.partial_update(ctx, clan_id, tag=first_tag)
    assert isinstance(data, ServiceError)
    assert data == ServiceError.CLANS_TAG_EXISTS


async def test_should_disband(ctx: Context):
    name = "Akatsuki Quafghjlity Co"
    tag = "AffQC"
    description = "The"
    owner = 19354
    join_method = JoinMethod.CLOSED

    data = await clans.create(ctx, name, tag, description, owner, join_method)
    assert not isinstance(data, ServiceError)
    assert data["clan_id"] is not None
    clan_id = data["clan_id"]

    data = await clans.disband(ctx, clan_id)
    assert not isinstance(data, ServiceError)

    data = await clans.fetch_one(ctx, clan_id)
    assert isinstance(data, ServiceError)
    assert data == ServiceError.CLANS_NOT_FOUND


async def test_should_fail_disband_no_clan(ctx: Context):
    data = await clans.disband(ctx, 0)
    assert isinstance(data, ServiceError)
    assert data == ServiceError.CLANS_NOT_FOUND