from fastapi import APIRouter

from app.schemas import (
    TokenPairSchema,
    UserCreateResponseSchema,
    UserCreateSchema,
    UserCredentialsSchema,
)
from app.services.auth import get_user_by_credentials
from app.services.jwt import create_token_pair
from app.services.user import create_user

router = APIRouter(prefix="/auth")


@router.post("/token", response_model=TokenPairSchema)
async def create_token(user_data: UserCredentialsSchema) -> TokenPairSchema:
    user = await get_user_by_credentials(user_data.username, user_data.password)

    return create_token_pair(user.id)


@router.post("/token/refresh")
async def refresh_token(token: str):
    return {"token": "dasd124fdasgsdgt$#@sda"}


@router.post("/registration", response_model=UserCreateResponseSchema)
async def registration_user(user_data: UserCreateSchema) -> UserCreateResponseSchema:
    await create_user(
        username=user_data.username, password=user_data.password, email=user_data.email
    )

    return {"username": user_data.username, "email": user_data.email}
