# Proposal: Quality Infrastructure Setup

## Intent

Establecer la base de calidad del proyecto lexlysaas: testing, linting, type checking y automation. Actualmente el proyecto no tiene ninguna herramienta de calidad configurada (no hay tests, linting, ni type checking), lo cual impide mantener estándares de código y detectar errores tempranamente.

## Scope

### In Scope
- **pyproject.toml completo**: dependencias de desarrollo (pytest, pytest-asyncio, ruff, mypy), scripts de ejecución (test, lint, typecheck), configuración de proyecto (version, description, authors)
- **ruff configuration**: configuración en pyproject.toml o .ruff.toml, reglas E, F, I, UP, B, C4, ignore justificado para código legacy
- **mypy configuration**: configuración en mypy.ini o pyproject.toml, strictness moderada (python_version 3.13), path: backend/
- **pre-commit hooks**: .pre-commit-config.yaml con hooks ruff, mypy, trailing-whitespace, end-of-file-fixer
- **Tests smoke básicos**: tests/test_health.py (endpoint /health), tests/test_clientes.py (CRUD básico clientes), conftest.py con fixtures de test

### Out of Scope
- Configuración de coverage reporting
- CI/CD pipeline (GitHub Actions, etc.)
- Tests de integración con Supabase
- Configuración de type checking para frontend

## Capabilities

### New Capabilities
- `quality-automation`: Sistema de calidad automatizado que incluye testing, linting, type checking y pre-commit hooks

### Modified Capabilities
- Ninguno (es infraestructura nueva, no modifica capacidades existentes)

## Approach

Empezar desde cero (no había tooling configurado). Priorizar configuración centralizada en pyproject.toml donde sea posible. Los tests iniciales deben pasar (smoke tests básicos que verifican estructura existente).

## Affected Areas

| Area | Impact | Description |
|------|--------|-------------|
| `pyproject.toml` | Modified | Completar con dependencias, scripts, y configuración de proyecto |
| `backend/` | Modified | Agregar type hints para mypy baseline |
| `tests/` | New | Crear directorio con tests smoke básicos |
| `.pre-commit-config.yaml` | New | Configurar pre-commit hooks |
| `.ruff.toml` o pyproject.toml section | New | Configuración de linting |
| `mypy.ini` o pyproject.toml section | New | Configuración de type checking |

## Risks

| Risk | Likelihood | Mitigation |
|------|------------|------------|
| Código legacy no pasa ruff/mypy | High | Usar ignore justificado, no forzar immediate fix |
| Configuration drift entre archivos | Low | Centralizar en pyproject.toml donde sea posible |
| Tests iniciales pueden fallar por dependencias faltantes | Medium | Verificar entorno antes de ejecutar |

## Rollback Plan

1. Eliminar pyproject.toml modificado (mantener backup del original vacío)
2. Eliminar .pre-commit-config.yaml
3. Eliminar .ruff.toml si existe
4. Eliminar mypy.ini si existe
5. Eliminar directorio tests/ completamente
6. Ejecutar `git checkout -- .` para revertir cambios

## Dependencies

- Python 3.13 disponible en entorno
- git para version control

## Success Criteria

- [ ] `pytest` ejecuta sin errores (smoke tests pasan)
- [ ] `ruff check` pasa sin errores (con ignores documentados)
- [ ] `mypy` corre sobre backend/ sin errores críticos (strictness moderada)
- [ ] `pre-commit run --all-files` ejecuta todos los hooks
- [ ] Scripts en pyproject.toml funcionan: `python -m pytest`, `python -m ruff`, `python -m mypy`