.PHONY: install hooks lint format test-unit test-integration check up down

install:
	uv sync

hooks:
	uv run pre-commit install

lint:
	uv run ruff check .
	uv run ruff format --check .
	uv run mypy app

format:
	uv run ruff check --fix .
	uv run ruff format .

test-unit:
	@uv run pytest tests/unit -q; code=$$?; \
	if [ $$code -eq 5 ]; then echo "Юнит-тестов пока нет — это нормально."; exit 0; fi; \
	exit $$code

# Требует поднятого сервиса (make up).
test-integration:
	@uv run pytest tests/integration -q; code=$$?; \
	if [ $$code -eq 5 ]; then echo "Своих интеграционных тестов пока нет — это нормально."; exit 0; fi; \
	exit $$code

# Требует поднятого сервиса (make up) — обязательные тесты преподавателя.
test-contract:
	uv run pytest contract_tests -v

check: lint test-unit

up:
	docker compose up -d --build

down:
	docker compose down -v
