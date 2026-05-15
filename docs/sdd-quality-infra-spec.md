# SDD: Quality Infrastructure Setup

## Title

Configuración de infraestructura de calidad para lexlysaas

## Description

Establecer la base de calidad del proyecto lexlysaas incluyendo testing con pytest, linting con ruff, type checking con mypy, y automatización con pre-commit hooks. El objetivo es detectar errores tempranamente y mantener estándares de código consistentes.

## Deliverables

### 1. pyproject.toml completo

**Description**: Configurar proyecto Python con todas las dependencias necesarias y scripts de ejecución.

**Requirements**:
- Versión de Python: `>=3.13`
- Nombre del proyecto: `lexlysaas`
- Versión inicial: `0.1.0`
- Dependencias de producción a mantener:
  - `sqlmodel>=0.0.38`
  - `asyncpg>=0.31.0`
  - `fastapi>=0.115.0` (latest stable)
  - `uvicorn[standard]>=0.34.0` (latest stable)
  - `supabase>=2.10.0` (latest stable)
  - `python-dotenv>=1.0.0`
  - `python-jose[cryptography]>=3.3.0`
  - `passlib[bcrypt]>=1.7.4`
  - `pydantic>=2.10.0` (latest, required by FastAPI)
  - `pydantic-settings>=2.8.0` (recommended for settings management)
  - `httpx>=0.28.0` (required for test client)
- Dependencias de desarrollo:
  - `pytest>=8.3.0`
  - `pytest-asyncio>=0.25.0`
  - `pytest-cov>=6.0.0` (opcional, para coverage)
  - `ruff>=0.9.0` (latest stable)
  - `mypy>=1.14.0` (latest stable)
  - `pre-commit>=4.1.0`
- Scripts de ejecución (deben funcionar con `python -m <script>`):
  - `test`: ejecuta pytest
  - `lint`: ejecuta ruff check
  - `typecheck`: ejecuta mypy
  - `format`: ejecuta ruff format
  - `check`: ejecuta lint + typecheck

**Acceptance Criteria**:
- [ ] pyproject.toml tiene todas las secciones requeridas (project, dependencies, dev-dependencies, scripts, tool.pytest, tool.ruff, tool.mypy)
- [ ] `python -m pytest` ejecuta sin errores
- [ ] `python -m ruff check` ejecuta sin errores
- [ ] `python -m mypy` ejecuta sin errores
- [ ] `python -m ruff format --check` funciona
- [ ] Las versiones especificadas son compatibles con Python 3.13

**Testing Scenarios**:
1. Ejecución de `python -m pytest` con empty tests directory debe completar sin errores
2. Ejecución de `python -m ruff check` debe completarse (puede tener warnings/ignores)
3. Ejecución de `python -m mypy backend/` debe completarse (puede tener errores no críticos)
4. Los scriptsshortcuts (`uv run test`, `uv run lint`, etc.) funcionan correctamente

---

### 2. ruff configuration

**Description**: Configuración de linting con reglas apropiadas para el proyecto.

**Requirements**:
- Archivo de configuración: `.ruff.toml` en raíz del proyecto
- Reglas habilitadas:
  - `E` (pycodestyle errors)
  - `F` (pyflakes)
  - `I` (isort)
  - `UP` (pyupgrade)
  - `B` (flake8-bugbear)
  - `C4` (flake8-comprehensions)
- Exclusiones:
  - `.venv/`
  - `node_modules/`
  - `.git/`
  - `__pycache__/`
  - `.pytest_cache/`
  - `backend/__pycache__/`
- Configuración adicional:
  - `line-length`: 100
  - `target-version`: py313
  - `fixable`: ["I", "UP", "B", "C4", "E", "F", "W"]
  - `unfixable`: [] (vacío permite fix todo lo posible)
  - `select`: ["E", "F", "I", "UP", "B", "C4"]

**Acceptance Criteria**:
- [ ] Archivo `.ruff.toml` existe en raíz del proyecto
- [ ] `ruff check .` ejecuta sin errores críticos (ignores documentados son aceptables)
- [ ] `ruff check --fix .` aplica autofix sin romper código
- [ ] `ruff format .` formatea correctamente
- [ ] Las exclusiones no incluyen código del proyecto

**Testing Scenarios**:
1. `ruff check backend/` debe completarse con exit code 0 (con ignores si aplica)
2. `ruff check --select E,F,I,UP,B,C4 backend/` sigue las reglas especificadas
3. `ruff format --check backend/` verifica formateo
4. Archivos en .venv son correctamente ignorados

---

### 3. mypy configuration

**Description**: Configuración de type checking con strictness moderada.

**Requirements**:
- Archivo de configuración: `mypy.ini` en raíz del proyecto
- Ruta a analizar: `backend/`
- Versión de Python: 3.13
- Opciones de strictness:
  - `python_version`: 3.13
  - `disallow_untyped_defs`: false (progressive typing)
  - `disallow_any_expr`: false
  - `warn_return_any`: true
  - `warn_unused_configs`: true
  - `warn_redundant_casts`: true
  - `strict_optional`: true
  - `no_implicit_optional`: true
  - `check_untyped_defs`: true
  - `disallow_untyped_calls`: false (permite llamadas a libs sin type hints)
- Ignores permitidos:
  - `[mypy-*.py]` sections para paths específicos
  - ignores documentados para código legacy

**Acceptance Criteria**:
- [ ] Archivo `mypy.ini` existe en raíz del proyecto
- [ ] `mypy backend/` ejecuta sin errores críticos (warnings aceptables)
- [ ] Configuración usa Python 3.13
- [ ] La opción `disallow_untyped_defs = false` está configurada
- [ ] No falla por falta de type hints en código legacy

**Testing Scenarios**:
1. `mypy backend/` debe completarse (puede tener errors no críticos)
2. `mypy --strict backend/` debe fallar gracefully (strict mode esperado que falle)
3. `mypy --config-file mypy.ini backend/` usa el archivo de configuración correcto
4. Warnings sobre missing type hints no bloquean la ejecución

---

### 4. pre-commit hooks

**Description**: Automatizar calidad de código en el momento del commit.

**Requirements**:
- Archivo: `.pre-commit-config.yaml` en raíz del proyecto
- Hooks requeridos:
  1. `trailing-whitespace`: elimina espacios al final de líneas
  2. `end-of-file-fixer`: asegura que archivos terminen con newline
  3. `check-yaml`: valida archivos YAML
  4. `check-json`: valida archivos JSON
  5. `ruff` (con `--fix`): aplica linting automatic
  6. `mypy`: type checking
- Stages: `commit` y `push`
- Configuración de ruff hook:
  - `args: ["--fix", "--exit-non-zero-on-fix"]`
  - `language: system` (usa ruff instalado en el sistema)
- Configuración de mypy hook:
  - `args: ["backend/"]`
  - `language: system`
  - `pass_filenames: false` (ejecuta sobre todo el path)
- Repositorios de hooks (using official pre-commit mirrors):
  - `repo: https://github.com/pre-commit/pre-commit-hooks`
  - `repo: https://github.com/astral-sh/ruff-pre-commit` (para ruff)
  - `repo: https://github.com/pre-commit/mirrors-mypy` (para mypy)

**Acceptance Criteria**:
- [ ] Archivo `.pre-commit-config.yaml` existe y es válido
- [ ] `pre-commit run --all-files` ejecuta todos los hooks
- [ ] `pre-commit install` instala los hooks correctamente
- [ ] Los hooks de ruff y mypy se ejecutan en commits
- [ ] Hooks de archivos triviales (trailing-whitespace, etc.) funcionan

**Testing Scenarios**:
1. `pre-commit run --all-files` ejecuta todos los hooks
2. `pre-commit run --all-files --show-diff-on-failure` muestra cambios
3. Commit con archivo con trailing-whitespace es rechazado o auto-fijado
4. `pre-commit autoupdate` actualiza los hooks correctamente
5. Hooks se ejecutan en staging (commit) y push

---

### 5. Tests smoke básicos

**Description**: Tests básicos que verifican que los endpoints fundamentales funcionan.

**Requirements**:
- Directorio: `tests/` en raíz del proyecto
- Estructura de archivos:
  - `tests/__init__.py` (puede estar vacío o con marker)
  - `tests/conftest.py` - fixtures de pytest
  - `tests/test_health.py` - tests del endpoint /health
  - `tests/test_clientes_crud.py` - tests del CRUD de clientes
- Configuración de pytest (en `pyproject.toml` sección `[tool.pytest.ini_options]`):
  - `asyncio_mode`: auto
  - `testpaths`: ["tests"]
  - `python_files`: ["test_*.py"]
  - `python_classes`: ["Test*"]
  - `python_functions`: ["test_*"]
- Fixture `client` en conftest.py:
  - Crea TestClient de FastAPI
  - Importa la app desde `backend.app.main`
  - Configura environment para testing (disable env vars de producción)
- Test `test_health.py`:
  - `test_health_returns_200`: GET /api/v1/health retorna 200
  - `test_health_returns_ok_status`: response.json["status"] == "ok"
  - `test_health_returns_version`: response.json contiene "version"
- Test `test_clientes_crud.py`:
  - `test_get_clientes_requires_auth`: GET /api/v1/clientes sin auth retorna 401
  - `test_clientes_endpoint_exists`: GET /api/v1/clientes existe (puede mockear auth)

**Acceptance Criteria**:
- [ ] Directorio `tests/` existe
- [ ] `tests/conftest.py` tiene el fixture `client` correctamente configurado
- [ ] `tests/test_health.py` pasa: GET /api/v1/health retorna 200 y {"status": "ok"}
- [ ] `tests/test_clientes_crud.py` pasa: endpoint existe y responde correctamente
- [ ] `pytest` ejecuta todos los tests sin errores
- [ ] Configuración pytest en pyproject.toml tiene `asyncio_mode = auto`

**Testing Scenarios**:
1. `pytest tests/` ejecuta todos los tests y pasan
2. `pytest tests/test_health.py -v` muestra resultados específicos
3. `pytest tests/ -v --tb=short` muestra output detallado
4. Test que hace request real a /api/v1/health verifica status code
5. Test de clientes verifica que el endpoint requiere autenticación

---

## Success Criteria

| Criteria | Verification |
|----------|--------------|
| pytest ejecuta sin errores | `pytest tests/ -v` returns 0 |
| ruff check pasa | `ruff check .` returns 0 |
| mypy corre sobre backend/ | `mypy backend/` completes |
| pre-commit run --all-files ejecuta | `pre-commit run --all-files` completes |
| Scripts en pyproject.toml funcionan | `python -m pytest`, `python -m ruff`, `python -m mypy` all work |

## Dependencies

- Python 3.13 disponible en entorno
- git para version control
- Las herramientas (pytest, ruff, mypy, pre-commit) se instalarán via pyproject.toml

## Risks and Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Código legacy no pasa ruff/mypy | High | Medium | Usar ignore justificado, documentar en archivos |
| Tests iniciales pueden fallar | Medium | Low | Verificar que endpoints existen antes de escribir tests |
| Configuration drift entre archivos | Low | Low | Centralizar en pyproject.toml donde sea posible |

## Rollback Plan

1. Eliminar/modificar `pyproject.toml` (mantener backup)
2. Eliminar `.pre-commit-config.yaml`
3. Eliminar `.ruff.toml`
4. Eliminar `mypy.ini`
5. Eliminar directorio `tests/` completamente
6. Ejecutar `git checkout -- .` para revertir cambios

## Notes

- La configuración sigue el principio de "progressive typing": mypy dimulai con strictness moderada y se ajusta gradualmente
- ruff se configura con autofix para reducir friction
- Los tests smoke usan TestClient de FastAPI para no requerir servidor corriendo
- Los hooks de pre-commit se ejecutan en staging para catchear problemas antes de commit