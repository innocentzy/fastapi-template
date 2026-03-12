import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_register_user(client: AsyncClient):
    response = await client.post(
        "/auth/register/user",
        json={
            "nickname": "New Test User",
            "password": "user",
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["nickname"] == "New Test User"
    assert "password" not in data


@pytest.mark.asyncio
async def test_register_duplicate_nickname(client: AsyncClient, test_user):
    response = await client.post(
        "auth/register/user",
        json={
            "nickname": "Test User",
            "password": "user",
        },
    )
    assert response.status_code == 400
    assert "already registered" in response.json()["detail"]


@pytest.mark.asyncio
async def test_login_success(client: AsyncClient, test_user):
    response = await client.post(
        "/auth/login",
        json={
            "nickname": "Test User",
            "password": "user",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["access_token"]["token_sign"] == "bearer"


@pytest.mark.asyncio
async def test_login_wrong_password(client: AsyncClient, test_user):
    response = await client.post(
        "/auth/login",
        json={
            "nickname": "Test User",
            "password": "wrong password",
        },
    )
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_login_nonexistent_user(client: AsyncClient):
    response = await client.post(
        "/auth/login",
        json={
            "nickname": "Non Existent",
            "password": "user",
        },
    )
    assert response.status_code == 404
