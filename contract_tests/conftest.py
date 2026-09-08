"""Контрактные тесты преподавателя. Не редактировать — файл защищён.

CI перед прогоном тестов заменяет всю папку contract_tests/ копией из
шаблона по тегу reference-v1 (см. .github/workflows/ci.yml) — правки
здесь на результат не влияют.

Обязательны только register и login (см. README). Остальные эндпоинты
контракта — refresh, user/update, user/history, logout, user/me —
вы проверяете своими интеграционными тестами в tests/integration/.
"""

import os
import time

import httpx
import pytest

BASE_URL = os.environ.get("AUTH_SERVICE_URL", "http://localhost:8002")


@pytest.fixture(scope="session")
def client() -> httpx.Client:
    with httpx.Client(base_url=BASE_URL, timeout=10.0) as c:
        _wait_until_healthy(c)
        yield c


def _wait_until_healthy(c: httpx.Client, attempts: int = 30, delay: float = 2.0) -> None:
    last_error: Exception | None = None
    for _ in range(attempts):
        try:
            resp = c.get("/health")
            if resp.status_code == 200:
                return
        except httpx.HTTPError as exc:
            last_error = exc
        time.sleep(delay)
    raise RuntimeError(
        f"Сервис по адресу {BASE_URL} не ответил 200 на /health за отведённое время"
    ) from last_error
