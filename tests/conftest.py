import os
import uuid
import pytest
import httpx

BASE_URL = os.getenv("BASE_URL", "http://localhost:8000")

@pytest.fixture(scope="session")
def base_url() -> str:
    return BASE_URL

@pytest.fixture()
def unique_email() -> str:
    return f"user_{uuid.uuid4().hex[:10]}@example.com"

@pytest.fixture()
def password() -> str:
    return "StrongPass123!"

@pytest.fixture()
def client(base_url: str):
    with httpx.Client(base_url=base_url, timeout=10.0) as c:
        yield c

def register(client: httpx.Client, email: str, password: str):
    r = client.post("/auth/register", json={"email": email, "password": password})
    assert r.status_code == 201, r.text
    return r.json()

def login(client: httpx.Client, email: str, password: str) -> str:
    r = client.post(
        "/auth/login",
        data={"username": email, "password": password},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert r.status_code == 200, r.text
    data = r.json()
    return data["access_token"]

@pytest.fixture()
def user_token(client, unique_email, password) -> str:
    register(client, unique_email, password)
    return login(client, unique_email, password)

@pytest.fixture()
def auth_headers(user_token: str):
    return {"Authorization": f"Bearer {user_token}"}
