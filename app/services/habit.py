from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import NotFoundException
from app.models.habit import Habit
from app.repositories import habit as habit_repo
from app.schemas.habit import HabitCreate, HabitUpdate


async def create_habit(
    session: AsyncSession, data: HabitCreate, user_id: UUID
) -> Habit:
    """Create a habit for the given user."""
    return await habit_repo.create_habit(
        session=session,
        user_id=user_id,
        title=data.title,
        description=data.description,
        days=data.days,
    )


async def get_habit(
    session: AsyncSession, habit_id: UUID, user_id: UUID
) -> Habit:
    """Gets a habit by its id. Throws NotFoundException if the habit is not found"""
    habit = await habit_repo.get_habit_by_id(session=session, habit_id=habit_id, user_id=user_id)
    if habit is None:
        raise NotFoundException(f"Habit {habit_id} not found") from None
    return habit


async def get_habits(session: AsyncSession, user_id: UUID) -> list[Habit]:
    """List habits belonging to the current user"""
    return await habit_repo.get_habits_by_user(session=session, user_id=user_id)


async def update_habit(
    session: AsyncSession, data: HabitUpdate, habit_id: UUID, user_id: UUID
) -> Habit:
    """Update habit for the given user"""
    habit = await get_habit(session=session, habit_id=habit_id, user_id=user_id)
    return await habit_repo.update_habit(session=session, habit=habit, data=data)


async def delete_habit(
    session: AsyncSession, habit_id: UUID, user_id: UUID
) -> None:
    """Delete habit for the given user"""
    habit = await get_habit(
        session=session, habit_id=habit_id, user_id=user_id
    )
    await habit_repo.delete_habit(session=session, habit=habit)
