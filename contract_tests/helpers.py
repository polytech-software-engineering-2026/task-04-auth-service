"""Общие хелперы контрактных тестов. Не редактировать — файл защищён."""

import uuid

import httpx


def unique_email() -> str:
    return f"user-{uuid.uuid4().hex}@example.com"


def register(
    client: httpx.Client, email: str | None = None, password: str = "correct-horse"
) -> dict:
    payload = {"email": email or unique_email(), "password": password}
    resp = client.post("/register", json=payload)
    assert resp.status_code == 201, resp.text
    return payload
