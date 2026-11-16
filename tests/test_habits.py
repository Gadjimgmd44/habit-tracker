async def test_create_habit(client, auth_headers):
    response = await client.post(
        "/api/v1/habits",
        json={"title": "Read book", "description": "10 pages", "days": ["Mon", "Wed"]},
        headers=auth_headers,
    )
    data = response.json()
    assert response.status_code == 201
    assert data["title"] == "Read book"
    assert data["description"] == "10 pages"
    assert data["days"] == ["Mon", "Wed"]
    assert "id" in data
    assert "created_at" in data
    assert "updated_at" in data
    assert "user_id" not in data


async def test_list_habits_empty(client, auth_headers):
    response = await client.get("/api/v1/habits", headers=auth_headers)
    assert response.status_code == 200
    assert response.json() == []


async def test_list_habits(client, auth_headers):
    await client.post(
        "/api/v1/habits",
        json={"title": "Read book", "description": "10 pages", "days": ["Mon", "Wed"]},
        headers=auth_headers,
    )
    response_get = await client.get("/api/v1/habits", headers=auth_headers)
    data = response_get.json()
    habit = data[0]
    assert response_get.status_code == 200
    assert habit["title"] == "Read book"
    assert habit["description"] == "10 pages"
    assert habit["days"] == ["Mon", "Wed"]


async def test_get_habit(client, auth_headers):
    response_create = await client.post(
        "/api/v1/habits",
        json={"title": "Read book", "description": "10 pages", "days": ["Mon", "Wed"]},
        headers=auth_headers,
    )
    habit_id = response_create.json()["id"]
    response_get = await client.get(f"/api/v1/habits/{habit_id}", headers=auth_headers)
    data = response_get.json()
    assert response_get.status_code == 200
    assert data["title"] == "Read book"
    assert data["description"] == "10 pages"
    assert data["days"] == ["Mon", "Wed"]


async def test_patch_habit(client, auth_headers):
    response_create = await client.post(
        "/api/v1/habits",
        json={"title": "Read book", "description": "10 pages", "days": ["Mon", "Wed"]},
        headers=auth_headers,
    )
    habit_id = response_create.json()["id"]
    response_patch = await client.patch(
        f"/api/v1/habits/{habit_id}",
        json={"description": "25 pages"},
        headers=auth_headers,
    )
    assert response_patch.status_code == 200
    data = response_patch.json()
    assert data["title"] == "Read book"
    assert data["description"] == "25 pages"
    assert data["days"] == ["Mon", "Wed"]


async def test_delete_habit(client, auth_headers):
    response_create = await client.post(
        "/api/v1/habits",
        json={"title": "Read book", "description": "10 pages", "days": ["Mon", "Wed"]},
        headers=auth_headers,
    )
    habit_id = response_create.json()["id"]
    response_delete = await client.delete(
        f"/api/v1/habits/{habit_id}", headers=auth_headers
    )
    assert response_delete.status_code == 204
    response_get = await client.get(f"/api/v1/habits/{habit_id}", headers=auth_headers)
    assert response_get.status_code == 404


async def test_create_habit_duplicate_days(client, auth_headers):
    response = await client.post(
        "/api/v1/habits",
        json={
            "title": "Read book",
            "description": "10 pages",
            "days": ["Mon", "Mon", "Wed"],
        },
        headers=auth_headers,
    )
    assert response.status_code == 422


async def test_create_habit_sorts_days(client, auth_headers):
    response = await client.post(
        "/api/v1/habits",
        json={
            "title": "Read book",
            "description": "10 pages",
            "days": ["Fri", "Mon", "Thu"],
        },
        headers=auth_headers,
    )
    data = response.json()
    assert response.status_code == 201
    assert data["days"] == ["Mon", "Thu", "Fri"]


async def test_get_foreign_habit(client, auth_headers, auth_headers_2):
    response_first = await client.post(
        "/api/v1/habits",
        json={
            "title": "Read book",
            "description": "10 pages",
            "days": ["Fri", "Mon", "Thu"],
        },
        headers=auth_headers,
    )
    habit_id = response_first.json()["id"]
    response_second = await client.get(
        f"/api/v1/habits/{habit_id}", headers=auth_headers_2
    )
    assert response_second.status_code == 404


async def test_patch_foreign_habit(client, auth_headers, auth_headers_2):
    response_first = await client.post(
        "/api/v1/habits",
        json={
            "title": "Read book",
            "description": "10 pages",
            "days": ["Fri", "Mon", "Thu"],
        },
        headers=auth_headers,
    )
    habit_id = response_first.json()["id"]
    response_second = await client.patch(
        f"/api/v1/habits/{habit_id}",
        json={"description": "false"},
        headers=auth_headers_2,
    )
    assert response_second.status_code == 404


async def test_delete_foreign_habit(client, auth_headers, auth_headers_2):
    response_first = await client.post(
        "/api/v1/habits",
        json={
            "title": "Read book",
            "description": "10 pages",
            "days": ["Fri", "Mon", "Thu"],
        },
        headers=auth_headers,
    )
    habit_id = response_first.json()["id"]
    response_second = await client.delete(
        f"/api/v1/habits/{habit_id}", headers=auth_headers_2
    )
    assert response_second.status_code == 404
