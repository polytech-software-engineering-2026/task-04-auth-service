import httpx

from contract_tests.helpers import register, unique_email


def test_login_success(client: httpx.Client) -> None:
    payload = register(client)
    resp = client.post("/login", json=payload)
    assert resp.status_code == 200, resp.text
    body = resp.json()
    assert "access_token" in body
    assert "refresh_token" in body
    assert body["token_type"].lower() == "bearer"


def test_login_wrong_password_returns_401(client: httpx.Client) -> None:
    payload = register(client)
    resp = client.post("/login", json={"email": payload["email"], "password": "wrong-password"})
    assert resp.status_code == 401


def test_login_nonexistent_user_returns_401(client: httpx.Client) -> None:
    resp = client.post("/login", json={"email": unique_email(), "password": "whatever"})
    assert resp.status_code == 401


def test_login_returns_different_tokens_each_time(client: httpx.Client) -> None:
    payload = register(client)
    first = client.post("/login", json=payload).json()
    second = client.post("/login", json=payload).json()
    assert first["access_token"] != second["access_token"]
    assert first["refresh_token"] != second["refresh_token"]
