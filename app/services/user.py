from sqlalchemy import select

from app.models import User
from app.orm.session import async_session_maker

from .auth import UserAlreadyExist, encrypt_password


async def create_user(username: str, password: str, email: str) -> User:
    async with async_session_maker() as session:
        query = select(User.username).where(User.username == username)
        user = await session.execute(query)
        user = user.scalars().first()
        if user is not None:
            raise UserAlreadyExist

        encrypted_password = str(encrypt_password(password))
        user = User(username=username, password=encrypted_password, email=email)
        session.add(user)

        await session.flush()
        await session.commit()

        return user
