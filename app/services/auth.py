from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import EmailAlreadyExists
from app.core.security import get_password_hash, verify_password
from app.models.user import User
from app.repositories.user import create_user, get_user_by_email
from app.schemas.user import UserCreate

DUMMY_HASH = get_password_hash("dummy")


async def register_user(session: AsyncSession, user: UserCreate) -> User:
    """Register a new user and return the created User instance."""
    existing_user = await get_user_by_email(session=session, email=user.email)
    if existing_user is not None:
        raise EmailAlreadyExists(f"Email {user.email} already registered")
    hashed = get_password_hash(user.password)
    try:
        return await create_user(session, email=user.email, hashed_password=hashed)
    except IntegrityError:
        await session.rollback()
        raise EmailAlreadyExists(f"Email {user.email} already registered")


async def authenticate_user(
    session: AsyncSession, email: str, password: str
) -> User | None:
    """Verify credentials. Returns User on success, None otherwise."""
    existing_user = await get_user_by_email(session, email)
    if existing_user is None:
        verify_password(password, DUMMY_HASH)
        return None
    if not verify_password(
        plain_password=password, hashed_password=existing_user.hashed_password
    ):
        return None
    return existing_user
