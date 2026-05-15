# Tasks: Arquitectura Hexagonal - Fase 1 (Fundaciones)

## Overview

Implementar las fundaciones de la arquitectura hexagonal: puertos abstractos, adaptadores concretos, e inyección de dependencias para demostrar el patrón con `ClienteService` como piloto.

## Prerequisites

- Leer `docs/sdd-hexagonal-design.md` completo antes de empezar
- Entender el Data Flow del diseño

---

## Task 1: Crear estructura de carpetas del dominio

**Descripción**: Crear los paquetes base de la arquitectura hexagonal (`domain/` e `infrastructure/`).

**Archivos a crear**:
- `backend/app/domain/__init__.py` — Package marker vacío
- `backend/app/domain/ports/__init__.py` — Exports del paquete ports
- `backend/app/infrastructure/__init__.py` — Package marker vacío
- `backend/app/infrastructure/adapters/__init__.py` — Exports del paquete adapters

**Criterios de Done**:
- [ ] Los 4 archivos existen con contenido válido en Python
- [ ] Los imports dentro de los `__init__.py` exponen las clases correctas
- [ ] `ruff check backend/app/domain/ backend/app/infrastructure/` no reporta errores

---

## Task 2: Crear Puerto Supabase (domain/ports/supabase_port.py)

**Descripción**: Definir la interfaz abstracta que abstrae el acceso a Supabase. Este es el contrato central de la Fase 1.

**Archivo a crear**: `backend/app/domain/ports/supabase_port.py`

**Contenido requerido**:
```python
from abc import ABC, abstractmethod
from typing import Any, Optional

class SupabasePort(ABC):
    @abstractmethod
    def get_one(self, table: str, filters: dict[str, Any]) -> Optional[dict[str, Any]]:
        """Retrieve a single record. Returns None if not found."""
        ...

    @abstractmethod
    def get_all(
        self,
        table: str,
        filters: dict[str, Any],
        limit: int = 100,
        offset: int = 0,
    ) -> list[dict[str, Any]]:
        """Retrieve multiple records with optional pagination."""
        ...

    @abstractmethod
    def insert(self, table: str, data: dict[str, Any]) -> dict[str, Any]:
        """Insert a record and return it."""
        ...

    @abstractmethod
    def update(
        self, table: str, filters: dict[str, Any], data: dict[str, Any]
    ) -> dict[str, Any]:
        """Update records matching filters and return updated record."""
        ...

    @abstractmethod
    def delete(self, table: str, filters: dict[str, Any]) -> bool:
        """Delete records matching filters. Returns True if any deleted."""
        ...
```

**Criterios de Done**:
- [ ] Clase hereda de `ABC`
- [ ] Los 5 métodos son `@abstractmethod`
- [ ] Tipado completo con `Optional`, `list`, `dict[str, Any]`
- [ ] `mypy backend/app/domain/ports/supabase_port.py` pasa sin errores

---

## Task 3: Crear Adaptador Supabase (infrastructure/adapters/supabase_adapter.py)

**Descripción**: Implementación concreta del `SupabasePort` que usa el cliente real de Supabase.

**Archivo a crear**: `backend/app/infrastructure/adapters/supabase_adapter.py`

**Contenido requerido**:
- Clase `SupabaseClientAdapter(SupabasePort)`
- `__init__(self, client: Client)` — guardar `_client`
- Implementar los 5 métodos delegando a `self._client.table().*`
- Manejo de respuestas vacías: `response.data[0] if response.data else None`
- En `delete`: verificar que al menos 1 registro fue eliminado

**Criterios de Done**:
- [ ] Hereda de `SupabasePort`
- [ ] `__init__` recibe el cliente Supabase
- [ ] Cada método delega correctamente al cliente
- [ ] Manejo de casos vacíos (sin datos = None/False)
- [ ] Import correcto de `supabase.Client`

---

## Task 4: Actualizar deps.py con providers

**Descripción**: Agregar la función `get_supabase_adapter()` al archivo de dependencias de FastAPI.

**Archivo a modificar**: `backend/app/api/deps.py`

**Cambios requeridos**:
1. Agregar imports:
   ```python
   from backend.app.domain.ports.supabase_port import SupabasePort
   from backend.app.infrastructure.adapters.supabase_adapter import SupabaseClientAdapter
   ```

2. Agregar función:
   ```python
   def get_supabase_adapter() -> SupabasePort:
       """Provides a SupabaseClientAdapter instance."""
       return SupabaseClientAdapter(get_supabase())
   ```

**Criterios de Done**:
- [ ] Import del `SupabasePort` agregado
- [ ] Import del `SupabaseClientAdapter` agregado
- [ ] Función `get_supabase_adapter()` definida
- [ ] Backward compatibility: `get_supabase()` sigue existiendo
- [ ] `ruff check backend/app/api/deps.py` pasa

---

## Task 5: Refactorizar ClienteService

**Descripción**: Modificar `ClienteService` para usar el puerto abstracto via inyección de dependencias.

**Archivo a modificar**: `backend/app/services/cliente_service.py`

**Cambios requeridos**:
1. Agregar imports:
   ```python
   from backend.app.domain.ports.supabase_port import SupabasePort
   from backend.app.infrastructure.adapters.supabase_adapter import SupabaseClientAdapter
   ```

2. Modificar `__init__`:
   ```python
   def __init__(self, supabase_port: SupabasePort | None = None):
       if supabase_port is not None:
           self._supabase_port = supabase_port
       else:
           self._supabase_port = SupabaseClientAdapter(get_supabase())
   ```

3. Cambiar todos los `get_supabase()` internos por `self._supabase_port`

**Criterios de Done**:
- [ ] Constructor acepta `SupabasePort | None`
- [ ] Valor default crea `SupabaseClientAdapter` internally (backward compat)
- [ ] `get_supabase()` ya no se llama dentro de los métodos públicos
- [ ] La interfaz pública (`get_all`, `get_by_id`, `create`, `update`, `delete`) no cambia
- [ ] Tests existentes siguen pasando (backward compat)

---

## Task 6: Actualizar endpoints de clientes

**Descripción**: Modificar los endpoints de la API para usar inyección de dependencias con el puerto.

**Archivo a modificar**: `backend/app/api/clientes.py`

**Cambios requeridos**:
1. Agregar imports:
   ```python
   from backend.app.domain.ports.supabase_port import SupabasePort
   from backend.app.api.deps import get_supabase_adapter
   ```

2. En cada endpoint que use `ClienteService`:
   - Agregar parámetro: `supabase_port: SupabasePort = Depends(get_supabase_adapter)`
   - Cambiar: `ClienteService()` → `ClienteService(supabase_port)`

**Criterios de Done**:
- [ ] `get_supabase_adapter` importado
- [ ] Los 5 endpoints principales (`get_clientes`, `get_cliente`, `create_cliente`, `update_cliente`, `delete_cliente`) usan el patrón
- [ ] La firma de cada endpoint solo agrega el nuevo parámetro (no cambia comportamiento)
- [ ] `ruff check backend/app/api/clientes.py` pasa

---

## Task 7: Crear tests para el adapter

**Descripción**: Unit tests del `SupabaseClientAdapter` usando mocks.

**Archivo a crear**: `tests/test_supabase_adapter.py`

**Contenido requerido**:
```python
import unittest
from unittest.mock import MagicMock, patch
from backend.app.infrastructure.adapters.supabase_adapter import SupabaseClientAdapter

class TestSupabaseClientAdapter(unittest.TestCase):
    def setUp(self):
        self.mock_client = MagicMock()
        self.adapter = SupabaseClientAdapter(self.mock_client)

    def test_get_one_returns_record(self):
        # Arrange
        self.mock_client.table.return_value.select.return_value.eq.return_value.execute.return_value.data = [{"id": 1, "nombre": "Test"}]
        # Act
        result = self.adapter.get_one("test_table", {"id": 1})
        # Assert
        self.assertEqual(result, {"id": 1, "nombre": "Test"})

    def test_get_one_returns_none_when_empty(self):
        # Arrange
        self.mock_client.table.return_value.select.return_value.eq.return_value.execute.return_value.data = []
        # Act
        result = self.adapter.get_one("test_table", {"id": 1})
        # Assert
        self.assertIsNone(result)

    def test_get_all_returns_list(self):
        # Arrange
        self.mock_client.table.return_value.select.return_value.execute.return_value.data = [{"id": 1}, {"id": 2}]
        # Act
        result = self.adapter.get_all("test_table", {})
        # Assert
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 2)

    def test_insert_returns_created_record(self):
        # Arrange
        created = {"id": 1, "nombre": "New"}
        self.mock_client.table.return_value.insert.return_value.execute.return_value.data = [created]
        # Act
        result = self.adapter.insert("test_table", {"nombre": "New"})
        # Assert
        self.assertEqual(result, created)

    def test_update_returns_updated_record(self):
        # Arrange
        updated = {"id": 1, "nombre": "Updated"}
        self.mock_client.table.return_value.update.return_value.eq.return_value.execute.return_value.data = [updated]
        # Act
        result = self.adapter.update("test_table", {"id": 1}, {"nombre": "Updated"})
        # Assert
        self.assertEqual(result, updated)

    def test_delete_returns_true_when_deleted(self):
        # Arrange
        self.mock_client.table.return_value.delete.return_value.eq.return_value.execute.return_value.data = [{"id": 1}]
        # Act
        result = self.adapter.delete("test_table", {"id": 1})
        # Assert
        self.assertTrue(result)

    def test_delete_returns_false_when_not_found(self):
        # Arrange
        self.mock_client.table.return_value.delete.return_value.eq.return_value.execute.return_value.data = []
        # Act
        result = self.adapter.delete("test_table", {"id": 999})
        # Assert
        self.assertFalse(result)
```

**Criterios de Done**:
- [ ] 5 tests (uno por método CRUD) mínimo
- [ ] Cada test tiene Arrange-Act-Assert claro
- [ ] Usa `unittest.mock` (no pytest-mock)
- [ ] `pytest tests/test_supabase_adapter.py -v` pasa

---

## Task 8: Crear tests para ClienteService refactorizado

**Descripción**: Unit tests del `ClienteService` mockeando el `SupabasePort`.

**Archivo a crear**: `tests/test_cliente_service_refactored.py`

**Contenido requerido**:
```python
import pytest
from unittest.mock import MagicMock
from backend.app.services.cliente_service import ClienteService
from backend.app.domain.ports.supabase_port import SupabasePort

class TestClienteServiceWithMockedPort:
    def setup_method(self):
        self.mock_port = MagicMock(spec=SupabasePort)
        self.service = ClienteService(supabase_port=self.mock_port)

    def test_get_all_calls_port_get_all(self):
        self.mock_port.get_all.return_value = [{"id": 1}, {"id": 2}]
        result = self.service.get_all("user-123")
        self.mock_port.get_all.assert_called_once()
        assert len(result) == 2

    def test_get_by_id_calls_port_get_one(self):
        self.mock_port.get_one.return_value = {"id": 1, "nombre": "Test"}
        result = self.service.get_by_id("user-123", 1)
        self.mock_port.get_one.assert_called_once()
        assert result["id"] == 1

    def test_create_calls_port_insert(self):
        self.mock_port.insert.return_value = {"id": 1, "nombre": "New", "user_id": "user-123"}
        result = self.service.create("user-123", {"nombre": "New"})
        self.mock_port.insert.assert_called_once()
        assert result["id"] == 1

    def test_update_calls_port_update(self):
        self.mock_port.update.return_value = {"id": 1, "nombre": "Updated"}
        result = self.service.update("user-123", 1, {"nombre": "Updated"})
        self.mock_port.update.assert_called_once()
        assert result["nombre"] == "Updated"

    def test_delete_calls_port_delete(self):
        self.mock_port.delete.return_value = True
        result = self.service.delete("user-123", 1)
        self.mock_port.delete.assert_called_once()
        assert result is True

    def test_backward_compat_no_port_uses_default(self):
        """Test that ClienteService() without port still works (backward compat)"""
        # No pasar supabase_port — usa default interno
        service = ClienteService()
        # No debe lanzar excepción
        assert service is not None
```

**Criterios de Done**:
- [ ] 5+ tests cubriendo los métodos principales
- [ ] Mock de `SupabasePort` con `spec=SupabasePort`
- [ ] Test de backward compatibility (sin port)
- [ ] `pytest tests/test_cliente_service_refactored.py -v` pasa

---

## Task 9: Validar implementación completa

**Descripción**: Ejecutar todas las validaciones para asegurar que la implementación es correcta y no rompe código existente.

**Validaciones a ejecutar**:

```bash
# 1. Tests del nuevo código
pytest tests/test_supabase_adapter.py tests/test_cliente_service_refactored.py -v

# 2. Todos los tests existentes + nuevos
pytest tests/ -v

# 3. Linting
ruff check backend/app/

# 4. Type checking
mypy backend/app/domain/ backend/app/infrastructure/ backend/app/services/cliente_service.py

# 5. Verificar que endpoints funcionan (smoke test)
cd backend && uvicorn app.main:app --reload &
# Probar GET /api/v1/clientes con auth
# Probar POST /api/v1/clientes
# Verificar que responde igual que antes
```

**Criterios de Done**:
- [ ] Todos los tests pasan (`pytest tests/`)
- [ ] `ruff check` sin errores en archivos modificados/creados
- [ ] `mypy` sin errores en el código nuevo
- [ ] Endpoints responden correctamente (smoke test manual)

---

## Archivos Involucrados

| Tipo | Archivos |
|------|----------|
| **Crear** | `backend/app/domain/__init__.py` |
| | `backend/app/domain/ports/__init__.py` |
| | `backend/app/domain/ports/supabase_port.py` |
| | `backend/app/infrastructure/__init__.py` |
| | `backend/app/infrastructure/adapters/__init__.py` |
| | `backend/app/infrastructure/adapters/supabase_adapter.py` |
| | `tests/test_supabase_adapter.py` |
| | `tests/test_cliente_service_refactored.py` |
| **Modificar** | `backend/app/api/deps.py` |
| | `backend/app/services/cliente_service.py` |
| | `backend/app/api/clientes.py` |

## Orden de Ejecución

1. Task 1 → Task 2 → Task 3 → Task 4 → Task 5 → Task 6 → Task 7 → Task 8 → Task 9

> **Nota**: Las Tasks 1-3 crean la estructura base. Las Tasks 4-6 modifican el código existente. Las Tasks 7-8添加 tests. La Task 9 valida todo.

## Rollback Plan

Si algo falla, revertir:
- Archivos modificados → estado original de git
- Archivos nuevos → borrar con `rm`

El código legacy sigue funcionando porque no se eliminó nada.