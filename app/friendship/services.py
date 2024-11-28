from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.models import User
from app.friendship.schemas import FriendshipEntitySchema


async def search_friendship_entities(session: AsyncSession, search):
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
