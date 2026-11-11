from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.habit import Habit
from app.schemas.habit import DayName, HabitUpdate


async def create_habit(
    session: AsyncSession,
    *,
    user_id: UUID,
    title: str,
    description: str | None,
    days: list[DayName],
) -> Habit:
    """Create a new habit for the given user."""
    habit = Habit(user_id=user_id, title=title, description=description, days=days)
    session.add(habit)
    await session.commit()
    await session.refresh(habit)
    return habit


async def get_habits_by_user(session: AsyncSession, user_id: UUID) -> list[Habit]:
    """Get all habits belonging to the specified user."""
    result = await session.scalars(
        select(Habit).where(Habit.user_id == user_id).order_by(Habit.created_at.desc())
    )
    return result.all()


async def get_habit_by_id(
    session: AsyncSession, habit_id: UUID, user_id: UUID
) -> Habit | None:
    """Get a specific habit by its ID and user ID."""
    return await session.scalar(
        select(Habit).where(Habit.id == habit_id, Habit.user_id == user_id)
    )


async def update_habit(session: AsyncSession, habit: Habit, data: HabitUpdate) -> Habit:
    """Update an existing habit in the database."""
    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(habit, key, value)
    await session.commit()
    await session.refresh(habit)
    return habit


async def delete_habit(session: AsyncSession, habit: Habit) -> None:
    """Delete the given habit."""
    await session.delete(habit)
    await session.commit()
