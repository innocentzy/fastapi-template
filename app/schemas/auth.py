from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.models.auth import UserRole


class UserCreate(BaseModel):
    nickname: str = Field(..., min_length=3, max_length=100)
    password: str = Field(..., min_length=6, max_length=100)


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nickname: str
    role: UserRole
    created_at: datetime


class Token(BaseModel):
    value: str
    token_type: str
    token_sign: str = "bearer"


class TokenPair(BaseModel):
    access_token: Token
    refresh_token: Token


class LoginRequest(BaseModel):
    nickname: str
    password: str
