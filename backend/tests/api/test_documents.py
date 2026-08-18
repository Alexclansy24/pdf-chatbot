import uuid
import pytest


@pytest.mark.asyncio
async def test_list_documents(
    authenticated_client,
):

    response = await authenticated_client.get(
        "/api/v1/documents"
    )

    print("STATUS:", response.status_code)
    print("RESPONSE:", response.json())

    assert response.status_code == 200

@pytest.mark.asyncio
async def test_list_documents_requires_auth(
    client,
):

    response = await client.get(
        "/api/v1/documents"
    )

    assert response.status_code == 401

@pytest.mark.asyncio
async def test_get_document_not_found(
    authenticated_client,
):

    document_id = uuid.uuid4()

    response = await authenticated_client.get(
        f"/api/v1/documents/{document_id}"
    )

    assert response.status_code == 404

@pytest.mark.asyncio
async def test_get_document_requires_auth(
    client,
):

    document_id = uuid.uuid4()

    response = await client.get(
        f"/api/v1/documents/{document_id}"
    )

    assert response.status_code == 401