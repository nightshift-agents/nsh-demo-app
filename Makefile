UV ?= uv

.PHONY: install test lint format run

install:
	$(UV) sync

test:
	$(UV) run pytest

lint:
	$(UV) run ruff check .
	$(UV) run ruff format --check .

format:
	$(UV) run ruff check --fix .
	$(UV) run ruff format .

run:
	$(UV) run uvicorn app.main:app --reload --port 8000
