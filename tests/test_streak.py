from datetime import date, timedelta

from app.schemas.habit import DAY_ORDER
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


def test_calculate_current_streak_skip_days():
    result = calculate_current_streak(
        days=["Mon", "Wed", "Fri"],
        log_dates={
            date(2026, 1, 12),  # Mon
            date(2026, 1, 9),  # Fri
            date(2026, 1, 7),  # Wed
        },
        created_at=date(2026, 1, 1),
        today=date(2026, 1, 14),  # Wed
    )
    assert result == 3


async def test_complete_habit(client, today_name, auth_headers):
    create_response = await client.post(
        "/api/v1/habits",
        json={"title": "Read book", "description": "10 pages", "days": [today_name]},
        headers=auth_headers,
    )
    habit_id = create_response.json()["id"]
    response = await client.post(
        f"/api/v1/habits/{habit_id}/complete", headers=auth_headers
    )

    assert response.status_code == 201
    data = response.json()
    assert data["today_completed"] is True
    assert data["display_streak"] == 1


async def test_complete_wrong_day(client, today_name, auth_headers):
    wrong_day = next(day for day in DAY_ORDER if day != today_name)
    create_response = await client.post(
        "/api/v1/habits",
        json={"title": "Read book", "description": "10 pages", "days": [wrong_day]},
        headers=auth_headers,
    )
    habit_id = create_response.json()["id"]

    response = await client.post(
        f"/api/v1/habits/{habit_id}/complete", headers=auth_headers
    )

    assert response.status_code == 400
    assert "not scheduled" in response.json()["detail"].lower()


async def test_uncomplete_habit(client, today_name, auth_headers):
    create_response = await client.post(
        "/api/v1/habits",
        json={"title": "Read book", "description": "10 pages", "days": [today_name]},
        headers=auth_headers,
    )
    habit_id = create_response.json()["id"]

    complete_response = await client.post(
        f"/api/v1/habits/{habit_id}/complete", headers=auth_headers
    )
    assert complete_response.status_code == 201

    delete_response = await client.delete(
        f"/api/v1/habits/{habit_id}/complete", headers=auth_headers
    )
    assert delete_response.status_code == 204

    stats_response = await client.get(
        f"/api/v1/habits/{habit_id}/stats", headers=auth_headers
    )
    assert stats_response.status_code == 200

    stats = stats_response.json()
    assert stats["today_completed"] is False
    assert stats["display_streak"] == 0


async def test_uncomplete_no_log(client, today_name, auth_headers):
    create_response = await client.post(
        "/api/v1/habits",
        json={"title": "Read book", "description": "10 pages", "days": [today_name]},
        headers=auth_headers,
    )
    habit_id = create_response.json()["id"]

    response = await client.delete(
        f"/api/v1/habits/{habit_id}/complete", headers=auth_headers
    )

    assert response.status_code == 404
    assert "no completion log" in response.json()["detail"].lower()


async def test_stats_fields(client, today_name, auth_headers):
    create_response = await client.post(
        "/api/v1/habits",
        json={"title": "Read book", "description": "10 pages", "days": [today_name]},
        headers=auth_headers,
    )
    habit_id = create_response.json()["id"]

    response = await client.get(
        f"/api/v1/habits/{habit_id}/stats", headers=auth_headers
    )

    assert response.status_code == 200
    data = response.json()
    expected_fields = {
        "current_streak",
        "best_streak",
        "display_streak",
        "today_scheduled",
        "today_completed",
        "total_completions_history",
    }

    assert expected_fields.issubset(data.keys())
    assert data["today_scheduled"] is True
    assert data["today_completed"] is False
