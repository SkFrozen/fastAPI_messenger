from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.models import User
from app.friendship.models import Friendship
from app.friendship.schemas import FriendshipEntitySchema


class FriendshipNotFoundError(Exception):
    pass


async def get_user_friends(
    session: AsyncSession, user_id: int
) -> list[FriendshipEntitySchema]:
    """Get friends of a user."""
    query = (
        select(User.id, User.username, User.first_name, User.last_name)
        .join(Friendship, Friendship.friend_id == User.id)
        .where(Friendship.user_id == user_id)
    )
    result = await session.execute(query)

    return [
        FriendshipEntitySchema(
            id=row[0],
            username=row[1],
            first_name=row[2],
            last_name=row[3],
            type="user",
        )
        for row in result
    ]


async def search_friendship_entities(
    session: AsyncSession, search
) -> list[FriendshipEntitySchema]:
    query = select(User.id, User.username, User.first_name, User.last_name).where(
        User.username.ilike(f"%{search}%")
        | User.first_name.ilike(f"%{search}%")
        | User.last_name.ilike(f"%{search}%")
    )

    result = await session.execute(query)

    return [
        FriendshipEntitySchema(
            id=row[0],
            username=row[1],
            first_name=row[2],
            last_name=row[3],
            type="user",
        )
        for row in result
    ]


async def create_friendship_entity(
    session: AsyncSession, user_id: int, friend_username: str
) -> FriendshipEntitySchema:
    friend = (
        await session.execute(select(User).where(User.username == friend_username))
    ).scalar_one_or_none()

    if friend is None:
        raise FriendshipNotFoundError("User not found")

    friendship = Friendship(user_id=user_id, friend_id=friend.id)
    friendship_schema = FriendshipEntitySchema(
        id=friend.id,
        username=friend.username,
        first_name=friend.first_name,
        last_name=friend.last_name,
        type="user",
    )

    session.add(friendship)
    try:
        await session.commit()
    except IntegrityError:
        pass

    return friendship_schema
