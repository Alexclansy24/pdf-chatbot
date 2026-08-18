from services.documents.repository import DocumentRepository
import uuid

import pytest
import pytest_asyncio

from httpx import ASGITransport, AsyncClient

from main import app


@pytest.fixture
def sample_text():
    return """
    LangGraph is a framework for building
    stateful applications with language models.
    """


@pytest_asyncio.fixture
async def client():

    transport = ASGITransport(
        app=app,
    )

    async with AsyncClient(
        transport=transport,
        base_url="http://test",
    ) as client:

        yield client


@pytest_asyncio.fixture
async def authenticated_client(client):

    email = (
        f"api_test_{uuid.uuid4().hex}"
        "@example.com"
    )

    password = "TestPassword123!"

    # Register test user
    register_response = await client.post(
        "/api/v1/auth/register",
        json={
            "email": email,
            "name": "API Test User",
            "password": password,
        },
    )

    assert register_response.status_code == 201

    # Login
    login_response = await client.post(
        "/api/v1/auth/login",
        json={
            "email": email,
            "password": password,
        },
    )

    assert login_response.status_code == 200

    token_data = login_response.json()

    access_token = token_data["access_token"]

    client.headers.update(
        {
            "Authorization":
                f"Bearer {access_token}"
        }
    )

    return client

@pytest_asyncio.fixture
async def test_document(authenticated_client):

    # Get the authenticated user's ID
    me_response = await authenticated_client.get(
        "/api/v1/auth/me"
    )

    assert me_response.status_code == 200

    user_id = me_response.json()["id"]

    repository = DocumentRepository()

    document = await repository.create(
        filename="test-document.pdf",
        storage_path="documents/test-document.pdf",
        user_id=uuid.UUID(user_id),
    )

    return document