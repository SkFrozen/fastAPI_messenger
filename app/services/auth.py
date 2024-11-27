from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from sqlalchemy import select

from app.models import User
from app.orm.session import async_session_maker
from app.settings import SECRET_KEY


class AuthError(Exception):
    pass


class InvalidTokenError(AuthError):
    pass


class UserAlreadyExist(AuthError):
    pass


class UserDoesNotExist(AuthError):
    pass


async def get_user_by_credentials(username: str, password: str) -> User:
    async with async_session_maker() as session:
        query = select(User).where(User.username == username)
        user = await session.execute(query)
        user = user.scalars().first()
        if user is not None:
            if check_password(password=password, encrypted_password=user.password):
                return user
        raise UserDoesNotExist


key = SECRET_KEY[:16].encode("utf-8")

aes = AES.new(key, AES.MODE_ECB)


def encrypt_password(password: str) -> bytes:
    """Encrypt password using AES"""
    password = password.encode("utf-8")
    padded_password = pad(password, AES.block_size)

    encrypted_password = aes.encrypt(padded_password)
    return encrypted_password


def check_password(password: str, encrypted_password: str) -> bool:
    """Check password using AES"""
    return encrypted_password == encrypt_password(password)
