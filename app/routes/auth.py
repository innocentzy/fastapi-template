from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import create_user, get_user_by_nickname
from app.database import get_db
from app.models.auth import TokenType, UserRole
from app.schemas.auth import LoginRequest, Token, TokenPair, UserCreate, UserResponse
from app.security import (
    create_access_token,
    create_refresh_token,
    decode_token,
    verify_password,
)


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    "/register/{role}", response_model=UserResponse, status_code=status.HTTP_201_CREATED
)
async def register(
    role: UserRole, user: UserCreate, db: AsyncSession = Depends(get_db)
):
    if await get_user_by_nickname(db, user.nickname):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Nickname already registered.",
        )
    return await create_user(db, user, role)


@router.post("/login", response_model=TokenPair)
async def login(credentials: LoginRequest, db: AsyncSession = Depends(get_db)):
    user = await get_user_by_nickname(db, credentials.nickname)
    if not user or not verify_password(credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Incorrect nickname or password.",
        )
    access_token = create_access_token(data={"sub": str(user.id)})
    refresh_token = create_refresh_token(data={"sub": str(user.id)})
    return {
        "access_token": Token(value=access_token),
        "refresh_token": Token(value=refresh_token),
    }


@router.post("/update-token", response_model=TokenPair)
async def update_token(token: Token):
    payload = decode_token(token.value)
    if not payload or payload.get("type") != TokenType.REFRESH:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token.",
        )

    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload.",
        )
    access_token = create_access_token(data={"sub": str(user_id)})
    refresh_token = create_refresh_token(data={"sub": str(user_id)})
    return {
        "access_token": Token(value=access_token),
        "refresh_token": Token(value=refresh_token),
    }
