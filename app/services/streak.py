from datetime import date, timedelta

from app.schemas.habit import DAY_ORDER


def _streak_ending_at(end_date, days, log_dates, created_at):
    current_date = end_date - timedelta(days=0)
    streak = 0
    while current_date >= created_at:
        day_name = DAY_ORDER[current_date.weekday()]
        if day_name not in days:
            current_date -= timedelta(days=1)
            continue
        if current_date in log_dates:
            streak += 1
            current_date -= timedelta(days=1)
            continue
        break
    return streak


def calculate_current_streak(
    days: list[str], log_dates: set[date], created_at: date, today: date
) -> int:
    """Calculate current streak excluding today.

    Walks backwards from yesterday until a scheduled day without a log is found
    or until habit creation date is reached.
    """
    return _streak_ending_at(today - timedelta(days=1), days, log_dates, created_at)


def calculate_display_streak(current_streak: int, today_completed: bool) -> int:
    """Return the streak to display to the user, including today if completed."""
    if today_completed:
        return current_streak + 1
    return current_streak


def calculate_best_streak(
    days: list[str], log_dates: set[date], created_at: date, today: date
) -> int:
    if not log_dates:
        return 0
    return max(_streak_ending_at(d, days, log_dates, created_at) for d in log_dates)
