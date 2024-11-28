from fastapi import APIRouter, Depends, Query

from app.auth.services.auth import get_user
from app.orm.session import get_session

from .schemas import FriendshipEntitySchema, NewFriendshipEntitySchema
from .services import (
    create_friendship_entity,
    get_user_friends,
    search_friendship_entities,
)

router = APIRouter(prefix="/friendships", tags=["friendships"])


@router.get("", response_model=list[FriendshipEntitySchema])
async def get_friendships_api_view(
    user=Depends(get_user), session=Depends(get_session)
):
    return await get_user_friends(session, user.id)


@router.get("/search", response_model=list[FriendshipEntitySchema])
async def search_friendships(
    search: str = Query("", min_length=3, max_length=50),
    _=Depends(get_user),
    session=Depends(get_session),
) -> list[FriendshipEntitySchema]:
    return await search_friendship_entities(session, search)


@router.post("", response_model=FriendshipEntitySchema)
async def create_friendship_api_view(
    friend_data: NewFriendshipEntitySchema,
    user=Depends(get_user),
    session=Depends(get_session),
):
    return await create_friendship_entity(session, user.id, friend_data.username)
