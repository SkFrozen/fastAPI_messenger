from fastapi import APIRouter

from app.schemas import TokenPairSchema, UserCredentialsSchema
from app.services.auth import get_user_by_credentials
from app.services.jwt import create_token_pair

router = APIRouter(prefix="/auth")


@router.post("/token", response_model=TokenPairSchema)
async def create_token(user_data: UserCredentialsSchema):
    user = await get_user_by_credentials(user_data.username, user_data.password)

    return create_token_pair(user.id)


@router.post("/token/refresh")
async def refresh_token(token: str):
    return {"token": "dasd124fdasgsdgt$#@sda"}
