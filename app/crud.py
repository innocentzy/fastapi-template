from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession

from app.security import get_password_hash
from app.models.auth import User, UserRole
from app.schemas.auth import UserCreate


async def get_user(db: AsyncSession, user_id: int) -> User | None:
    result = await db.execute(select(User).where(User.id == user_id))
    return result.scalar_one_or_none()


async def create_user(db: AsyncSession, user: UserCreate, role: UserRole) -> User:
    if role == UserRole.ADMIN:
        raise PermissionError("You are not allowed to create an admin user.")
    if role not in UserRole:
        raise ValueError("Invalid role.")
    hashed_password = get_password_hash(user.password)
    db_user = User(nickname=user.nickname, password=user.password, role=role)
    db.add(db_user)
    await db.flush()
    await db.refresh(db_user)
    return db_user


async def get_user_by_nickname(db: AsyncSession, nickname: str) -> User | None:
    result = await db.execute(select(User).where(User.nickname == nickname))
    return result.scalar_one_or_none()
