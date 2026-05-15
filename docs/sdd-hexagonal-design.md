# Design: Arquitectura Hexagonal - Fase 1 (Fundaciones)

## Technical Approach

Establecer las bases de la arquitectura hexagonal mediante la creación de un **puerto abstracto** (`SupabasePort`) y su **adaptador concreto** (`SupabaseClientAdapter`), utilizando la inyección de dependencias nativa de FastAPI (`Depends()`) — **sin librerías adicionales**. El servicio `ClienteService` será el piloto que demuestre el patrón.

## Architecture Decisions

### Decision: Puerto como interfaz abstracta (ABC)

**Choice**: `abc.ABC` con `@abstractmethod`
**Alternatives considered**: Protocol de typing (más flexible pero menos explícito), duck typing (sin contrato compile-time)
**Rationale**: ABC fuerza implementación completa en subclasses y falla en instanciación si faltan métodos. El IDE/autocomplete funciona mejor. mypy valida completamente.

### Decision: DI nativo de FastAPI (no library)

**Choice**: FastAPI `Depends()` sin container
**Alternatives considered**: `dependency-injector`, `lag`, `punq`
**Rationale**: El codebase no usa ningún contenedor DI. Añadir una librería introduce dependencia nueva. FastAPI `Depends()` es suficiente para este caso y es el patrón idiomático de FastAPI.

### Decision: Backward compatibility en ClienteService

**Choice**: Constructor con default `supabase_port: SupabasePort | None = None`
**Alternatives considered**: Solo nuevo constructor (breaking change), factory method
**Rationale**: Permite que el código legacy que hace `ClienteService()` siga funcionando durante la transición. El default crea internamente el adapter real.

## Data Flow

```
HTTP Request
     │
     ▼
┌─────────────────────────────────────────────────┐
│  FastAPI Depends(get_supabase_adapter)           │
│         │                                       │
│         ▼                                       │
│  SupabaseClientAdapter (infrastructure)        │
│         │                                       │
│         ▼                                       │
│  SupabasePort (domain/ports) ← abstracción      │
└─────────────────────────────────────────────────┘
     │
     ▼
┌─────────────────────────────────────────────────┐
│  ClienteService (domain/services)               │
│  usa self.supabase_port → get_one/get_all/...   │
└─────────────────────────────────────────────────┘
```

## File Changes

| File | Action | Description |
|------|--------|-------------|
| `backend/app/domain/__init__.py` | Create | Package marker |
| `backend/app/domain/ports/__init__.py` | Create | Exports SupabasePort |
| `backend/app/domain/ports/supabase_port.py` | Create | Puerto abstracto (ABC) |
| `backend/app/infrastructure/__init__.py` | Create | Package marker |
| `backend/app/infrastructure/adapters/__init__.py` | Create | Exports SupabaseClientAdapter |
| `backend/app/infrastructure/adapters/supabase_adapter.py` | Create | Adaptador concreto |
| `backend/app/api/deps.py` | Modify | Agregar `get_supabase_adapter()` |
| `backend/app/services/cliente_service.py` | Modify | Usar DI del puerto |
| `backend/app/api/clientes.py` | Modify | Inyectar via Depends |
| `tests/test_supabase_adapter.py` | Create | Unit tests del adapter |
| `tests/test_cliente_service.py` | Create | Unit tests del servicio refactorizado |

**Nota**: No se borra código legacy. El archivo `cliente_service.py` mantiene `get_supabase()` interna para backward compatibility del default del constructor.

## Interfaces / Contracts

### SupabasePort (abstract)

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

### SupabaseClientAdapter (concrete)

```python
from supabase import Client
from backend.app.domain.ports.supabase_port import SupabasePort

class SupabaseClientAdapter(SupabasePort):
    def __init__(self, client: Client):
        self._client = client

    def get_one(self, table: str, filters: dict[str, Any]) -> Optional[dict[str, Any]]:
        query = self._client.table(table).select("*")
        for key, value in filters.items():
            query = query.eq(key, value)
        response = query.execute()
        return response.data[0] if response.data else None
    # ... similar for get_all, insert, update, delete
```

### deps.py additions

```python
from backend.app.domain.ports.supabase_port import SupabasePort
from backend.app.infrastructure.adapters.supabase_adapter import SupabaseClientAdapter
from backend.app.api.deps import get_supabase

def get_supabase_adapter() -> SupabasePort:
    """Provides a SupabaseClientAdapter instance."""
    return SupabaseClientAdapter(get_supabase())
```

### ClienteService refactorizado

```python
class ClienteService:
    def __init__(self, supabase_port: SupabasePort | None = None):
        self._port = supabase_port or SupabaseClientAdapter(get_supabase())

    async def get_all(self, user_id: str) -> list[dict[str, Any]]:
        return self._port.get_all("clientes", {}, limit=1000)
```

### Endpoint actualizado

```python
from backend.app.domain.ports.supabase_port import SupabasePort
from backend.app.api.deps import get_supabase_adapter

@router.get("/clientes")
async def get_clientes(
    current_user: dict = Depends(get_current_user),
    supabase: SupabasePort = Depends(get_supabase_adapter),
):
    service = ClienteService(supabase)
    return await service.get_all(current_user["sub"])
```

## Testing Strategy

| Layer | What to Test | Approach |
|-------|-------------|----------|
| Unit | SupabaseClientAdapter methods | `unittest.mock.Mock` — mockear `_client` interno |
| Unit | ClienteService con mock del puerto | Mockear `SupabasePort` directamente |
| Integration | `/api/v1/clientes` con auth | pytest fixture con auth token real |

## Migration / Rollback

**No migration required** — pure architecture refactor. Código legacy coexiste en paralelo.

Rollback: revertir los 4 archivos modificados a su estado anterior. Los nuevos archivos (domain/, infrastructure/, tests/) quedan como código inerte pero no afectan al sistema.

## Open Questions

- [ ] **Cobertura mínima**: ¿70% de coverage sobre cuáles archivos — solo el nuevo código o incluyendo servicios migrados? → **Nuevo código** (`domain/` + `infrastructure/`) más `ClienteService` refactorizado.
- [ ] **Excepciones personalizadas**: ¿Crear excepciones propias del dominio (e.g., `RecordNotFoundError`) o propagar las de Supabase? → **Propagar Supabase**, convertir a `HTTPException` en la capa de API. Fase 1 solo inyecta abstracción, no rediseña el manejo de errores.

---

**Size estimate**: ~200 líneas de código nuevo. Bajo riesgo de impacto en reviewer. Single PR suficiente.
