from pydantic import BaseModel, Field


class UserCredentialsSchema(BaseModel):
    username: str = Field(..., max_length=150)
    password: str = Field(..., max_length=128)


class TokenPairSchema(BaseModel):
    access_token: str
    refresh_token: str


class AccessTokenSchema(BaseModel):
    access_token: str


class UpdateAccessTokenSchema(BaseModel):
    refresh_token: str


class UserCreateSchema(BaseModel):
    username: str = Field(..., max_length=150)
    email: str = Field(..., max_length=150)
    password: str = Field(..., max_length=128)


class UserCreateResponseSchema(BaseModel):
    username: str = Field(..., max_length=150)
    email: str = Field(..., max_length=150)
