import pytest


@pytest.mark.asyncio
async def test_root(client):

    response = await client.get("/")

    assert response.status_code == 200

    data = response.json()

    assert data["success"] is True

    assert data["message"] == "PDF Chatbot API"

    assert data["data"] == {}