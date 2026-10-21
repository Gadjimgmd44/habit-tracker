from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User


async def create_user(
    session: AsyncSession, *, email: str, hashed_password: str
) -> User:
    user = User(email=email, hashed_password=hashed_password)
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


async def get_user_by_email(session: AsyncSession, email: str) -> User | None:
    """Fetch user by email, returns None if not found."""
    return await session.scalar(select(User).where(User.email == email))


async def get_user_by_id(session: AsyncSession, user_id: UUID) -> User | None:
    """Fetch user by id, returns None if not found."""
    return await session.get(User, user_id)
