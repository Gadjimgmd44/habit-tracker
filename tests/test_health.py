async def test_session_works(db_session):
    from sqlalchemy import text

    result = await db_session.execute(text("SELECT 1"))
    assert result.scalar() == 1


async def test_client_works(client):
    response = await client.get("/docs")
    assert response.status_code == 200
