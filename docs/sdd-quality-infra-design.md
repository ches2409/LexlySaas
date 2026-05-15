# Design: Quality Infrastructure Setup

## Change

**Name**: quality-infra
**Mode**: hybrid (filesystem + Engram)
**Project**: lexlysaas
**Path**: `/media/chesdevos/CHESDEVS1/proyectos/lexlySaas`

## Technical Approach

Extender `pyproject.toml` existente con tooling de calidad (pytest, ruff, mypy, pre-commit). Cada archivo de configuración es independiente; el orden de implementación es por dependencias: pyproject.toml primero (base), luego cada archivo de configuración, finalmente los tests de smoke como validación del stack completo.

## Architecture Decisions

### Decision: pyproject.toml como fuente única de verdad

**Choice**: Definir `[tool.pytest]`, `[tool.ruff]` y `[tool.mypy]` en `pyproject.toml` en vez de archivos separados.
**Alternatives considered**: Archivos `.ruff.toml`, `mypy.ini` separados — ruff y mypy soportan `pyproject.toml` natively.
**Rationale**: Consolida configuración en un solo lugar, más fácil de mantener. Las secciones `[tool.*]` en pyproject.toml son el estándar moderno en la comunidad Python. Los archivos separados `.ruff.toml` y `mypy.ini` se crean SOLO si hay conflictos de nombres de sección o necesidad de paths distintos.

### Decision: Progressive typing con mypy

**Choice**: `disallow_untyped_defs = false` con `warn_return_any = true`.
**Alternatives considered**: Strict mode completo desde el inicio — rechazado porque el código legacy no tiene type hints completos.
**Rationale**: Captura errores de retorno sin bloquear por definiciones sin tipo. Se ajusta gradualmente con el proyecto.

### Decision: ruff como linter único

**Choice**: ruff con reglas E, F, I, UP, B, C4 — sinflake8 ni pyflakes separados.
**Alternatives considered**: Configurar flake8 + isort + pyupgrade por separado — rechazado porque ruff los reemplaza y es 10-100x más rápido.
**Rationale**: Una sola herramienta, configuración unificada, ejecución instantánea. No hay necesidad de múltiples linters cuando ruff los consolida.

### Decision: pre-commit con language: system

**Choice**: `language: system` para ruff y mypy en pre-commit hooks.
**Alternatives considered**: `language: python` con entry points — más portable pero requiere pip install de las tools.
**Rationale**: Asume que uv manage las herramientas en el entorno. `language: system` evita duplicar instalaciones y usa las herramientas ya disponibles en el PATH. Si el entorno no tiene ruff/mypy instalados globalmente, fallará — pero `uv sync` resuelve eso.

### Decision: TestClient de FastAPI para tests de smoke

**Choice**: No usar servidor real; TestClient importa `app` directamente.
**Alternatives considered**: httpx async client contra uvicorn corriendo — más realista pero más complejo.
**Rationale**: TestClient maneja el lifecycle de la app en memoria. No requiere servidor, no requiere ports, no tiene race conditions. Suficiente para smoke tests del endpoint de health y autenticación.

## Data Flow

```
pytest → conftest.py → TestClient → backend.app.main → app
              ↓
         fixtures: client (TestClient instance)
              ↓
tests/test_health.py → GET /api/v1/health → {"status": "ok", ...}
tests/test_clientes_crud.py → GET /api/v1/clientes → 401 (sin auth)
```

## File Changes

| File | Action | Description |
|------|--------|-------------|
| `pyproject.toml` | Modify | Agregar dependencies de dev, scripts, y tool sections |
| `.ruff.toml` | Create | Configuración standalone de ruff (backup, también en pyproject.toml) |
| `mypy.ini` | Create | Configuración standalone de mypy |
| `.pre-commit-config.yaml` | Create | Hooks de pre-commit |
| `tests/__init__.py` | Create | Package marker |
| `tests/conftest.py` | Create | Fixtures: client (TestClient) |
| `tests/test_health.py` | Create | Tests smoke para /api/v1/health |
| `tests/test_clientes_crud.py` | Create | Tests smoke para CRUD de clientes |

## Interfaces / Contracts

### pyproject.toml (update)

```toml
[project]
name = "lexlysaas"
version = "0.1.0"
description = "SaaS de gestión jurídica para despachos de extranjería"
requires-python = ">=3.13"
dependencies = [
    "asyncpg>=0.31.0",
    "sqlmodel>=0.0.38",
    "fastapi>=0.115.0",
    "uvicorn[standard]>=0.34.0",
    "supabase>=2.10.0",
    "python-dotenv>=1.0.0",
    "python-jose[cryptography]>=3.3.0",
    "passlib[bcrypt]>=1.7.4",
    "pydantic>=2.10.0",
    "pydantic-settings>=2.8.0",
    "httpx>=0.28.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.3.0",
    "pytest-asyncio>=0.25.0",
    "pytest-cov>=6.0.0",
    "ruff>=0.9.0",
    "mypy>=1.14.0",
    "pre-commit>=4.1.0",
]

[project.scripts]
test = "pytest"
lint = "ruff check ."
typecheck = "mypy backend/"
format = "ruff format ."
check = "sh -c 'uv run lint && uv run typecheck'"

[tool.pytest.ini_options]
asyncio_mode = "auto"
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]

[tool.ruff]
line-length = 100
target-version = "py313"
fixable = ["I", "UP", "B", "C4", "E", "F", "W"]
unfixable = []
select = ["E", "F", "I", "UP", "B", "C4"]

[tool.mypy]
python_version = "3.13"
disallow_untyped_defs = false
warn_return_any = true
warn_unused_configs = true
warn_redundant_casts = true
strict_optional = true
no_implicit_optional = true
check_untyped_defs = true
disallow_untyped_calls = false
```

### .ruff.toml (standalone)

```toml
line-length = 100
target-version = "py313"
fixable = ["I", "UP", "B", "C4", "E", "F", "W"]
unfixable = []
select = ["E", "F", "I", "UP", "B", "C4"]

exclude = [
    ".venv/",
    "node_modules/",
    ".git/",
    "__pycache__/",
    ".pytest_cache/",
    "backend/__pycache__/",
]
```

### mypy.ini (standalone)

```ini
[mypy]
python_version = 3.13
disallow_untyped_defs = False
warn_return_any = True
warn_unused_configs = True
warn_redundant_casts = True
strict_optional = True
no_implicit_optional = True
check_untyped_defs = True
disallow_untyped_calls = False
```

### .pre-commit-config.yaml

```yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v5.0.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-json

  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.9.0
    hooks:
      - id: ruff
        args: ["--fix", "--exit-non-zero-on-fix"]
      - id: ruff-format

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.14.0
    hooks:
      - id: mypy
        args: ["backend/"]
        pass_filenames: false
```

### tests/conftest.py

```python
"""Pytest fixtures para lexlysaas"""
from fastapi.testclient import TestClient
from backend.app.main import app
import os

# Desactivar carga de .env de producción en tests
os.environ["SUPABASE_URL"] = "https://test.supabase.co"
os.environ["SUPABASE_ANON_KEY"] = "test-key"
os.environ["JWT_SECRET"] = "test-secret"
os.environ["DATABASE_URL"] = "postgresql://test:test@localhost/test"

@pytest.fixture
def client():
    """TestClient de la app FastAPI"""
    with TestClient(app) as c:
        yield c
```

### tests/__init__.py

```python
"""Tests package for lexlysaas"""
```

### tests/test_health.py

```python
"""Smoke tests para el endpoint /health"""
import pytest

def test_health_returns_200(client):
    """GET /api/v1/health retorna 200"""
    response = client.get("/api/v1/health")
    assert response.status_code == 200

def test_health_returns_ok_status(client):
    """La respuesta contiene status: ok"""
    response = client.get("/api/v1/health")
    assert response.json()["status"] == "ok"

def test_health_returns_version(client):
    """La respuesta contiene el campo version"""
    response = client.get("/api/v1/health")
    assert "version" in response.json()
```

### tests/test_clientes_crud.py

```python
"""Smoke tests para el CRUD de clientes"""
import pytest

def test_get_clientes_requires_auth(client):
    """GET /api/v1/clientes sin auth retorna 401"""
    response = client.get("/api/v1/clientes")
    assert response.status_code == 401

def test_clientes_endpoint_exists(client):
    """El endpoint /api/v1/clientes existe y responde"""
    response = client.get("/api/v1/clientes")
    # 401 es esperado porque no hay token — pero el endpoint existe
    assert response.status_code in [401, 403]
```

## Testing Strategy

| Layer | What to Test | Approach |
|-------|-------------|----------|
| Smoke | Endpoints health y clientes existen | TestClient, asserts de status code |
| Lint | Código fuente pasa ruff check | `ruff check backend/` |
| Type | Tipos en backend/ son correctos | `mypy backend/` |
| Format | Código formateado consistentemente | `ruff format --check backend/` |
| Pre-commit | Hooks ejecutan en commit/push | `pre-commit run --all-files` |

## Migration / Rollout

No migration required — es configuración pura de tooling. El rollback es reversível deletando los archivos creados y ejecutando `git checkout -- pyproject.toml`.

## Open Questions

- [x] ¿Usar archivos separados o pyproject.toml? **Decisión**: pyproject.toml como primario, .ruff.toml y mypy.ini como backup/standalone.
- [ ] ¿El entorno tiene Python 3.13 instalado? Verificar antes de aplicar.
- [ ] ¿pre-commit está instalado globalmente? Si no, `uv tool install pre-commit` antes de `pre-commit install`.

## Order of Implementation

1. `pyproject.toml` — base del sistema (dependencias + scripts)
2. `.ruff.toml` — configuración standalone de ruff
3. `mypy.ini` — configuración standalone de mypy
4. `.pre-commit-config.yaml` — automatización
5. `tests/conftest.py`, `tests/__init__.py`, `tests/test_health.py`, `tests/test_clientes_crud.py` — validación

Dependencias: cada paso es independiente excepto que los tests dependen de pyproject.toml estar completo.