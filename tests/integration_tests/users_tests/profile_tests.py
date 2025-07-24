import pytest


@pytest.mark.asyncio
async def test_user_profile(authorized_client):
    """Test getting current user profile"""
    response = await authorized_client.get("/api/v1/me")
    assert response.status_code == 200
    data = response.json()
    assert "username" in data
