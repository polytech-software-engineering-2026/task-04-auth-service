import httpx

from contract_tests.helpers import register, unique_email


def test_register_success(client: httpx.Client) -> None:
    email = unique_email()
    resp = client.post("/register", json={"email": email, "password": "correct-horse"})
    assert resp.status_code == 201, resp.text
    body = resp.json()
    assert body["email"] == email
    assert "id" in body


def test_register_duplicate_email_returns_409(client: httpx.Client) -> None:
    payload = register(client)
    resp = client.post("/register", json=payload)
    assert resp.status_code == 409


def test_register_missing_password_returns_422(client: httpx.Client) -> None:
    resp = client.post("/register", json={"email": unique_email()})
    assert resp.status_code == 422


def test_register_missing_email_returns_422(client: httpx.Client) -> None:
    resp = client.post("/register", json={"password": "correct-horse"})
    assert resp.status_code == 422
