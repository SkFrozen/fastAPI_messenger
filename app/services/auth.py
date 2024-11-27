from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User


async def get_user_by_credentials(username: str, password: str) -> User:
    return User(id=3, name=username, password=password)
