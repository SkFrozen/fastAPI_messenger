from fastapi import APIRouter, Depends, HTTPException

from app.auth.schemas import (
    AccessTokenSchema,
    TokenPairSchema,
    UpdateAccessTokenSchema,
    UserCreateResponseSchema,
    UserCreateSchema,
    UserCredentialsSchema,
)
from app.auth.services.exc import AuthError
from app.orm.session import get_session

from .services.auth import create_user, get_user_by_credentials
from .services.jwt import create_token_pair, refresh_token

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/token", response_model=TokenPairSchema)
async def create_token_api_view(
    user_data: UserCredentialsSchema, session=Depends(get_session)
):
    try:
        user = await get_user_by_credentials(
            session, user_data.username, user_data.password
        )
    except AuthError as exc:
        raise HTTPException(status_code=400, detail=str(exc))

    return create_token_pair(user.id)


@router.post("/token/refresh", response_model=AccessTokenSchema)
async def refresh_token_api_view(
    user_data: UpdateAccessTokenSchema,
):
    try:
        access_token: AccessTokenSchema = refresh_token(user_data.refresh_token)
    except AuthError as exc:
        raise HTTPException(status_code=400, detail=str(exc))

    return access_token


@router.post("/registration", response_model=UserCreateResponseSchema)
async def registration_user_api_view(
    user_data: UserCreateSchema, session=Depends(get_session)
):
    try:
        user = await create_user(
            session=session,
            username=user_data.username,
            password=user_data.password,
            email=user_data.email,
        )
    except AuthError as exc:
        raise HTTPException(status_code=400, detail=str(exc))

    return UserCreateResponseSchema(username=user.username, email=user.email)
