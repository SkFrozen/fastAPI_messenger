from fastapi import APIRouter, Depends, Query

from app.auth.services.auth import get_user
from app.friendship.schemas import FriendshipEntitySchema
from app.friendship.services import search_friendship_entities
from app.orm.session import get_session

router = APIRouter(prefix="/friendships", tags=["friendships"])


@router.get("/search", response_model=list[FriendshipEntitySchema])
async def search_friendships(
    search: str = Query("", min_length=3, max_length=50),
    _=Depends(get_user),
    session=Depends(get_session),
) -> list[FriendshipEntitySchema]:
    return await search_friendship_entities(session, search)


@router.post("", response_model=list[FriendshipEntitySchema])
async def create_friendship(data):
    pass
