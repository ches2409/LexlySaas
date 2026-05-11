.PHONY: dev install lint test

# Desarrollo
dev:
	uv run uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload

# Instalación de dependencias
install:
	uv sync

# Linting
lint:
	uv run ruff check backend/

# Tests
test:
	uv run pytest

# Help
help:
	@grep -E '^[a-zA-Z_-]+:' Makefile | sed 's/:.*//' | sed 's/^/  /'
