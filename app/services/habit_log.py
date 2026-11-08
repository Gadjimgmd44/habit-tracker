from datetime import date
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import (
    AlreadyCompletedException,
    NotFoundException,
    NotScheduledTodayException,
)
from app.models.habit_log import HabitLog
from app.repositories import habit_log as habit_log_repo
from app.schemas.habit import DAY_ORDER, HabitStats
from app.services import streak as habit_streak_service
from app.services.habit import get_habit


async def complete_habit(
    session: AsyncSession, habit_id: UUID, user_id: UUID
) -> HabitLog:
    """Mark the habit as completed for today."""
    habit = await get_habit(session=session, habit_id=habit_id, user_id=user_id)
    today_date = date.today()  # noqa: DTZ011
    today_name = DAY_ORDER[today_date.weekday()]
    if today_name not in habit.days:
        raise NotScheduledTodayException(
            f"Habit is not scheduled for {today_name} ({today_date})"
        ) from None
    existing = await habit_log_repo.get_log_for_date(
        session=session, completed_at=today_date, habit_id=habit_id
    )
    if existing is not None:
        raise AlreadyCompletedException(
            f"Habit already completed on {today_date}"
        ) from None
    return await habit_log_repo.create_habit_log(
        session=session, habit_id=habit_id, completed_at=today_date
    )


async def uncomplete_habit(
    session: AsyncSession, habit_id: UUID, user_id: UUID
) -> None:
    """Remove the completion log for today."""
    await get_habit(session=session, habit_id=habit_id, user_id=user_id)
    today_date = date.today()  # noqa: DTZ011
    habit_day = await habit_log_repo.get_log_for_date(
        session=session, completed_at=today_date, habit_id=habit_id
    )
    if habit_day is None:
        raise NotFoundException("No completion log for today") from None
    await habit_log_repo.delete_log(session=session, habit_log=habit_day)


async def get_habit_stats(
    session: AsyncSession, habit_id: UUID, user_id: UUID
) -> HabitStats:
    habit = await get_habit(session=session, habit_id=habit_id, user_id=user_id)
    logs = await habit_log_repo.get_logs_from_habit(session=session, habit_id=habit_id)
    today_date = date.today()  # noqa: DTZ011
    today_name = DAY_ORDER[today_date.weekday()]
    log_dates = {log.completed_at for log in logs}
    today_scheduled = today_name in habit.days
    today_completed = today_date in log_dates
    created_date = habit.created_at.date()
    best_streak = habit_streak_service.calculate_best_streak(
        days=habit.days, log_dates=log_dates, created_at=created_date
    )
    current_streak = habit_streak_service.calculate_current_streak(
        days=habit.days, log_dates=log_dates, created_at=created_date, today=today_date
    )
    display_streak = habit_streak_service.calculate_display_streak(
        current_streak=current_streak, today_completed=today_completed
    )
    return HabitStats(
        current_streak=current_streak,
        best_streak=best_streak,
        display_streak=display_streak,
        today_completed=today_completed,
        today_scheduled=today_scheduled,
        total_completions_history=len(logs),
    )
