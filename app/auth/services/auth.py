from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.models import User
from app.orm.session import get_session

from .ext import InvalidCredentialsError, UserAlreadyExist
from .jwt import _get_user_from_token, auth_scheme
from .tools import check_email, check_password, encrypt_password


async def get_user_by_credentials(
    session: AsyncSession, username: str, password: str
) -> User:

    query = select(User).where(User.username == username)
    user = await session.execute(query)
    user = user.scalar_one_or_none()
    if user is not None:
        if check_password(password=password, encrypted_password=user.password):
            return user
    raise InvalidCredentialsError("Invalid username or password")


async def get_user(
    token: str = Depends(auth_scheme), session: AsyncSession = Depends(get_session)
) -> User:
    user_id = _get_user_from_token(token)
    query = select(User).where(User.id == user_id)
    try:
        user = (await session.execute(query)).scalar_one()
    except NoResultFound:
        raise InvalidCredentialsError("User not found")

    return user


async def create_user(
    session: AsyncSession, username: str, password: str, email: str
) -> User:
    if not check_email(email):
        raise InvalidCredentialsError("Invalid email")

    query = select(User.username).where(User.username == username)
    user = await session.execute(query)
    user = user.scalars().first()
    if user is not None:
        raise UserAlreadyExist("Username already exist")

    encrypted_password: str = encrypt_password(password)
    user = User(username=username, password=encrypted_password, email=email)
    session.add(user)

    await session.commit()
    await session.refresh(user)

    return user
