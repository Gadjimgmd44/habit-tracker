# успешная регистрация
# дубль email
# неверный пароль
# невалидный email
# слишком короткий пароль
# успешный логин
# Логин с несуществующим email
# Normalize email — проверка, что TEST@EXAMPLE.COM сохраняется как test@example.com
# Доступ к защищённому эндпоинту без токена
# Доступ с невалидным токеном
# Доступ с валидным токеном


async def test_register_success(client):
    response = await client.post(
        "/api/v1/auth/register",
        json={"email": "test@example.com", "password": "secret123"},
    )
    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert data["email"] == "test@example.com"
    assert "created_at" in data
    assert "hashed_password" not in data


async def test_register_duplicate_email(client):
    response_first = await client.post(
        "/api/v1/auth/register",
        json={"email": "test@example.com", "password": "secret123"},
    )
    assert response_first.status_code == 201
    response_second = await client.post(
        "/api/v1/auth/register",
        json={"email": "test@example.com", "password": "secret123"},
    )
    assert response_second.status_code == 409
    data = response_second.json()
    assert "already" in data["detail"].lower()


async def test_login_wrong_password(client):
    await client.post(
        "/api/v1/auth/register",
        json={"email": "test@example.com", "password": "secret123"},
    )
    response = await client.post(
        "/api/v1/auth/login",
        data={"username": "test@example.com", "password": "password_with_mistake"},
    )
    assert response.status_code == 401
    assert "incorrect" in response.json()["detail"].lower()


async def test_login_wrong_email(client):
    await client.post(
        "/api/v1/auth/register",
        json={"email": "test@example.com", "password": "secret123"},
    )

    response = await client.post(
        "/api/v1/auth/login",
        data={"username": "wrong@example.com", "password": "secret123"},
    )
    assert response.status_code == 401
    assert "incorrect" in response.json()["detail"].lower()


async def test_invalid_email(client):
    response = await client.post(
        "/api/v1/auth/register", json={"email": "wrongmail", "password": "secret123"}
    )
    assert response.status_code == 422


async def test_too_short_password(client):
    response = await client.post(
        "/api/v1/auth/register",
        json={"email": "test@example.com", "password": "1"},
    )
    assert response.status_code == 422


async def test_success_login(client):
    reponse_reg = await client.post(
        "/api/v1/auth/register",
        json={"email": "test@example.com", "password": "secret123"},
    )
    reponse_login = await client.post(
        "/api/v1/auth/login",
        data={"username": "test@example.com", "password": "secret123"},
    )
    assert reponse_reg.status_code == 201
    assert reponse_login.status_code == 200


async def test_normalize_email(client):
    response_reg = await client.post(
        "/api/v1/auth/register",
        json={"email": " TEST@example.com ", "password": "secret123"},
    )
    response_login = await client.post(
        "/api/v1/auth/login",
        data={"username": "test@example.com", "password": "secret123"},
    )
    assert response_reg.status_code == 201
    assert response_login.status_code == 200


async def test_protected_no_token(client):
    response = await client.get("/api/v1/habits")
    assert response.status_code == 401


async def test_protected_invalid_token(client):
    response = await client.get(
        "/api/v1/habits",
        headers={"Authorization": "Bearer garbage.token.here"},
    )
    assert response.status_code == 401


async def test_protected_valid_token(client):
    await client.post(
        "/api/v1/auth/register",
        json={"email": "test@example.com", "password": "secret123"},
    )
    login = await client.post(
        "/api/v1/auth/login",
        data={"username": "test@example.com", "password": "secret123"},
    )
    token = login.json()["access_token"]

    response = await client.get(
        "/api/v1/habits",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    assert response.json() == []
