# Tasks: Quality Infrastructure Setup

## Review Workload Forecast

| Field | Value |
|-------|-------|
| Estimated changed lines | ~200 (pyproject.toml updates + 4 config files + 4 test files) |
| 400-line budget risk | Low |
| Chained PRs recommended | No |
| Suggested split | Single PR |
| Delivery strategy | ask-on-risk |
| Chain strategy | pending |

Decision needed before apply: No
Chained PRs recommended: No
Chain strategy: pending
400-line budget risk: Low

### Suggested Work Units

| Unit | Goal | Likely PR | Notes |
|------|------|-----------|-------|
| 1 | Quality tooling config | PR 1 | pyproject.toml, .ruff.toml, mypy.ini, .pre-commit-config.yaml |
| 2 | Smoke tests | PR 1 | tests/ — validación del stack |

Single PR — los 6 archivos de configuración son independientes entre sí y los tests son validación.

## Phase 1: pyproject.toml (base)

- [ ] 1.1 Actualizar `[project]` en `pyproject.toml`: description = "SaaS de gestión jurídica para despachos de extranjería"
- [ ] 1.2 Reemplazar `dependencies = [...]` con todas las dependencias existentes del design (asyncpg, sqlmodel, fastapi, uvicorn, supabase, python-dotenv, python-jose, passlib, pydantic, pydantic-settings, httpx)
- [ ] 1.3 Agregar `[project.optional-dependencies]` con dev = pytest, pytest-asyncio, pytest-cov, ruff, mypy, pre-commit
- [ ] 1.4 Agregar `[project.scripts]` con test, lint, typecheck, format, check
- [ ] 1.5 Agregar `[tool.pytest.ini_options]` con asyncio_mode="auto", testpaths, python_files/classes/functions
- [ ] 1.6 Agregar `[tool.ruff]` con line-length=100, target-version="py313", fixable, unfixable, select
- [ ] 1.7 Agregar `[tool.mypy]` con python_version="3.13", disallow_untyped_defs=false, warn_return_any=true, y demás opciones del design

## Phase 2: Config files

- [ ] 2.1 Crear `.ruff.toml` con target-version="py313", line-length=100, select=["E","F","I","UP","B","C4"] y exclude paths
- [ ] 2.2 Crear `mypy.ini` con python_version=3.13, disallow_untyped_defs=False, warn_return_any=True, y demás opciones del design
- [ ] 2.3 Crear `.pre-commit-config.yaml` con pre-commit-hooks (trailing-whitespace, end-of-file-fixer, check-yaml, check-json), ruff (--fix), ruff-format, mypy (backend/)

## Phase 3: Tests

- [ ] 3.1 Crear `tests/__init__.py` con docstring "Tests package for lexlysaas"
- [ ] 3.2 Crear `tests/conftest.py` con fixture `client` (TestClient de FastAPI) y env vars de test
- [ ] 3.3 Crear `tests/test_health.py` con test_health_returns_200, test_health_returns_ok_status, test_health_returns_version
- [ ] 3.4 Crear `tests/test_clientes_crud.py` con test_get_clientes_requires_auth y test_clientes_endpoint_exists

## Phase 4: Validation

- [ ] 4.1 Ejecutar `uv run test` — verificar que pasa
- [ ] 4.2 Ejecutar `uv run lint` — verificar que pasa (o con ignores si hay errores menores)
- [ ] 4.3 Ejecutar `uv run typecheck` — verificar que pasa
- [ ] 4.4 Ejecutar `uv run check` — verificar que pasa

## Files Summary

| Task | File | Action | Done Criteria |
|------|------|---------|---------------|
| 1.1 | pyproject.toml | Modify | `[project]` name/version/description actualizados |
| 1.2 | pyproject.toml | Modify | Todas las dependencies presentes |
| 1.3 | pyproject.toml | Modify | `[project.optional-dependencies]` dev completo |
| 1.4 | pyproject.toml | Modify | `[project.scripts]` con los 5 scripts |
| 1.5 | pyproject.toml | Modify | `[tool.pytest.ini_options]` completo |
| 1.6 | pyproject.toml | Modify | `[tool.ruff]` completo |
| 1.7 | pyproject.toml | Modify | `[tool.mypy]` completo |
| 2.1 | .ruff.toml | Create | Archivo existe con config del design |
| 2.2 | mypy.ini | Create | Archivo existe con config del design |
| 2.3 | .pre-commit-config.yaml | Create | 4 hooks configurados con language: system |
| 3.1 | tests/__init__.py | Create | Package marker creado |
| 3.2 | tests/conftest.py | Create | Fixture client creado con env vars de test |
| 3.3 | tests/test_health.py | Create | 3 tests de smoke para /api/v1/health |
| 3.4 | tests/test_clientes_crud.py | Create | 2 tests de smoke para /api/v1/clientes |
| 4.1 | tests/ | Verify | `uv run test` pasa |
| 4.2 | . | Verify | `uv run lint` pasa |
| 4.3 | backend/ | Verify | `uv run typecheck` pasa |
| 4.4 | . | Verify | `uv run check` pasa |
