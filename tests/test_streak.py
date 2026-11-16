from datetime import date, timedelta

from app.services.streak import (
    calculate_best_streak,
    calculate_current_streak,
    calculate_display_streak,
)

today = date(2026, 1, 14)


def test_calculate_current_streak_empty():
    result = calculate_current_streak(
        days=["Mon"],
        log_dates=set(),
        created_at=date(2026, 1, 1),
        today=date(2026, 1, 10),
    )
    assert result == 0


def test_calculate_current_streak_full():
    result = calculate_current_streak(
        days=["Mon"],
        log_dates={
            today - timedelta(days=2),
            today - timedelta(days=9),
            today - timedelta(days=16),
        },
        created_at=today - timedelta(days=30),
        today=today,
    )
    assert result == 3


def test_calculate_current_streak_break():
    result = calculate_current_streak(
        days=["Mon"],
        log_dates={
            today - timedelta(days=2),
            today - timedelta(days=16),
        },
        created_at=today - timedelta(days=30),
        today=today,
    )
    assert result == 1


def test_calculate_display_streak_complete():
    result = calculate_display_streak(current_streak=5, today_completed=True)
    assert result == 6


def test_calculate_display_streak_not_complete():
    result = calculate_display_streak(current_streak=5, today_completed=False)
    assert result == 5


def test_calculate_best_streak():
    result = calculate_best_streak(
        days=["Mon"],
        log_dates={
            today - timedelta(days=1),
            today - timedelta(days=2),
            today - timedelta(days=9),
            today - timedelta(days=16),
            today - timedelta(days=20),
        },
        created_at=today - timedelta(days=30),
    )
    assert result == 3
