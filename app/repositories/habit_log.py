from datetime import date
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.habit_log import HabitLog


async def create_habit_log(
    session: AsyncSession, habit_id: UUID, completed_at: date
) -> HabitLog:
    """Create a habit completion log for the given habit and date."""
    habit_log = HabitLog(habit_id=habit_id, completed_at=completed_at)
    session.add(habit_log)
    await session.commit()
    await session.refresh(habit_log)
    return habit_log


async def get_logs_from_habit(session: AsyncSession, habit_id: UUID) -> list[HabitLog]:
    """Get all completion logs for a habit, newest first."""
    habit_logs = await session.scalars(
        select(HabitLog)
        .where(HabitLog.habit_id == habit_id)
        .order_by(HabitLog.completed_at.desc())
    )
    return list(habit_logs.all())


async def get_log_for_date(
    session: AsyncSession, completed_at: date, habit_id: UUID
) -> HabitLog | None:
    """Get a log for a specific habit and date."""
    habit_log = await session.scalar(
        select(HabitLog).where(
            HabitLog.completed_at == completed_at, HabitLog.habit_id == habit_id
        )
    )
    return habit_log


async def delete_log(session: AsyncSession, habit_log: HabitLog) -> None:
    """Delete the given habit log."""
    await session.delete(habit_log)
    await session.commit()
