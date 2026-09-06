.PHONY: install hooks lint format test check up down

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

test:
	uv run pytest tests -q

check: lint test

up:
	docker compose up -d --build

down:
	docker compose down -v
