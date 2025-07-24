import pytest


@pytest.mark.asyncio
async def test_ping(client):
    response = await client.get("/ping")
    assert response.status_code == 200
    assert response.text == '"Hoot!"'  # TODO: decode or something
