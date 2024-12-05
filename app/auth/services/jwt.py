from datetime import UTC, datetime, timedelta

from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from app.auth.schemas import AccessTokenSchema, TokenPairSchema
from app.settings import settings

from .exc import InvalidTokenError

auth_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/")
ALGORITHM = "HS256"
USER_IDENTIFIER = "user_id"
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes
REFRESH_TOKEN_EXPIRE_HOURS = settings.refresh_token_expire_hours
SECRET_KEY = settings.secret_key


def create_token_pair(user_id: int) -> TokenPairSchema:
    return TokenPairSchema(
        access_token=create_token(user_id, type_="access"),
        refresh_token=create_token(user_id, type_="refresh"),
    )


def create_token(user_id: int, type_: str):
    if type_ == "access":
        delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    else:
        delta = timedelta(days=REFRESH_TOKEN_EXPIRE_HOURS)

    return _create_jwt({"user_id": user_id, "type": type_}, delta)


def _create_jwt(payload: dict, delta: timedelta):
    expire = datetime.now(UTC) + delta
    payload.update({"exp": expire})
    return jwt.encode(payload, key=SECRET_KEY, algorithm=ALGORITHM)


def refresh_token(refresh_token: str):
    try:
        payload = jwt.decode(refresh_token, key=SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise InvalidTokenError("Invalid refresh token")
    if payload["type"] != "refresh":
        raise InvalidTokenError("Invalid token type")
    return AccessTokenSchema(
        access_token=create_token(payload["user_id"], type_="access")
    )


def _get_user_from_token(token: str) -> int:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise InvalidTokenError

    user_id = payload.get(USER_IDENTIFIER)

    if user_id is None:
        raise InvalidTokenError

    if not isinstance(user_id, int):
        raise InvalidTokenError

    return user_id
