# SDD: Arquitectura Hexagonal - Fase 1 (Fundaciones)

## Metadata

| Campo | Valor |
|-------|-------|
| **Title** | Arquitectura Hexagonal - Fase 1: Fundaciones |
| **Change** | hexagonal-architecture-fase1 |
| **Status** | Draft |
| **Created** | 2026-05-11 |

## Description

Establecer las bases de la arquitectura hexagonal creando abstracciones (puertos) e implementaciones (adaptadores) para la dependencia de Supabase. El objetivo es habilitar inyección de dependencias, mejorar la testabilidad, y eliminar los 7 lugares con `get_supabase()` duplicado en el backend actual.

---

## Deliverables

### 1. Puerto Supabase (SupabasePort)

**Ubicación**: `backend/app/domain/ports/supabase_port.py`

#### Descripción

Crear interfaz abstracta que defina operaciones CRUD sobre cualquier cliente de base de datos. Esta interfaz no tiene ninguna dependencia de Supabase — es puro Python/ABC.

#### Requisitos

| ID | Requisito | Tipo |
|----|-----------|------|
| REQ-01 | Crear clase abstracta `SupabasePort` que herede de `ABC` | Obligatorio |
| REQ-02 | Definir método `get_one(table: str, filters: dict) -> Optional[dict]` | Obligatorio |
| REQ-03 | Definir método `get_all(table: str, filters: dict, limit: int, offset: int) -> list[dict]` | Obligatorio |
| REQ-04 | Definir método `insert(table: str, data: dict) -> dict` | Obligatorio |
| REQ-05 | Definir método `update(table: str, filters: dict, data: dict) -> dict` | Obligatorio |
| REQ-06 | Definir método `delete(table: str, filters: dict) -> bool` | Obligatorio |
| REQ-07 | Usar `ABC` y `abstractmethod` del módulo `abc` | Obligatorio |
| REQ-08 | La interfaz no debe importar nada de `supabase` | Obligatorio |
| REQ-09 | Añadir docstrings a cada método con descripción y tipos | Obligatorio |
| REQ-10 | Manejar excepciones genéricas y retornar `None` cuando no hay resultados | Recomendado |

#### Criterios de Aceptación

| ID | Criterio | Condición |
|----|----------|-----------|
| ACC-01 | La interfaz es puro Python/ABC | No importar `supabase` ni ninguna librería externa |
| ACC-02 | Todos los métodos son `abstractmethod` | El interpreter lanza `TypeError` si se intenta instanciar directamente |
| ACC-03 | Tipos correcta | Pasar mypy sin errores |
| ACC-04 | Documentación | Todos los métodos tienen docstrings |

#### Escenarios de Testing

| Escenario | Input | Output Esperado |
|-----------|-------|-----------------|
| SC-01 | Instanciar directamente `SupabasePort` | `TypeError: Can't instantiate abstract class` |
| SC-02 | Subclase que no implementa todos los métodos | `TypeError` en tiempo de instanciación |
| SC-03 | Subclase que implementa todos los métodos | Instanciación exitosa |

---

### 2. Adaptador Supabase (SupabaseClientAdapter)

**Ubicación**: `backend/app/infrastructure/adapters/supabase_adapter.py`

#### Descripción

Implementar el puerto usando el cliente actual de Supabase. Este es el "adaptador" en términos de arquitectura hexagonal.

#### Requisitos

| ID | Requisito | Tipo |
|----|-----------|------|
| REQ-11 | Crear clase `SupabaseClientAdapter` que herede de `SupabasePort` | Obligatorio |
| REQ-12 | El constructor recibe una instancia de `Client` de Supabase | Obligatorio |
| REQ-13 | Implementar `get_one()` usando `table().select().eq().execute()` | Obligatorio |
| REQ-14 | Implementar `get_all()` usando `table().select().execute()` con límites | Obligatorio |
| REQ-15 | Implementar `insert()` usando `table().insert().execute()` | Obligatorio |
| REQ-16 | Implementar `update()` usando `table().update().eq().execute()` | Obligatorio |
| REQ-17 | Implementar `delete()` usando `table().delete().eq().execute()` | Obligatorio |
| REQ-18 | Manejar errores de Supabase y lanzar excepciones personalizadas | Recomendado |
| REQ-19 | El adapter debe ser importable desde `backend.app.infrastructure.adapters` | Obligatorio |

#### Criterios de Aceptación

| ID | Criterio | Condición |
|----|----------|-----------|
| ACC-05 | Implementa todos los métodos del puerto | Sin `NotImplementedError` |
| ACC-06 | Usa el cliente real de Supabase | `self.client.table(...).select(...)` |
| ACC-07 | Tests con mock pasan | Unit tests con `unittest.mock.Mock` |
| ACC-08 | Tipos pasan mypy | Sin errores de tipo |
| ACC-09 | Se puede inyectar en lugar del puerto abstracto | Duck typing funciona |

#### Escenarios de Testing

| Escenario | Input | Output Esperado |
|-----------|-------|-----------------|
| SC-04 | `get_one()` con filtro que existe | Retorna el dict del registro |
| SC-05 | `get_one()` con filtro que no existe | Retorna `None` |
| SC-06 | `get_all()` con límite 10 | Retorna lista de hasta 10 elementos |
| SC-07 | `insert()` con data válida | Retorna el registro creado |
| SC-08 | `update()` modifica campos | Retorna registro actualizado |
| SC-09 | `delete()` elimina registro | Retorna `True` |
| SC-10 | Error de conexión | Levanta excepción |

---

### 3. Reestructuración de Archivos

**Ubicación**: `backend/app/`

#### Descripción

Crear la estructura de carpetas para arquitectura hexagonal.

#### Estructura Requerida

```
backend/app/
├── domain/
│   ├── __init__.py
│   └── ports/
│       ├── __init__.py
│       └── supabase_port.py
├── infrastructure/
│   ├── __init__.py
│   └── adapters/
│       ├── __init__.py
│       └── supabase_adapter.py
```

#### Requisitos

| ID | Requisito | Tipo |
|----|-----------|------|
| REQ-20 | Crear carpeta `backend/app/domain/` | Obligatorio |
| REQ-21 | Crear carpeta `backend/app/domain/ports/` | Obligatorio |
| REQ-22 | Crear carpeta `backend/app/infrastructure/` | Obligatorio |
| REQ-23 | Crear carpeta `backend/app/infrastructure/adapters/` | Obligatorio |
| REQ-24 | Crear `__init__.py` en cada nivel de paquete | Obligatorio |
| REQ-25 | Exportar `SupabasePort` desde `backend.app.domain.ports` | Obligatorio |
| REQ-26 | Exportar `SupabaseClientAdapter` desde `backend.app.infrastructure.adapters` | Obligatorio |

#### Criterios de Aceptación

| ID | Criterio | Condición |
|----|----------|-----------|
| ACC-10 | Carpetas creadas | `ls domain/ports/` y `ls infrastructure/adapters/` funcionan |
| ACC-11 | Imports funcionan | `from backend.app.domain.ports import SupabasePort` sin error |
| ACC-12 | Estructura de paquetes Python | Ningún `__init__.py` falta |

#### Escenarios de Testing

| Escenario | Input | Output Esperado |
|-----------|-------|-----------------|
| SC-11 | Importar `SupabasePort` desde paquete | Sin error de importación |
| SC-12 | Importar `SupabaseClientAdapter` desde paquete | Sin error de importación |
| SC-13 | `python -c "import backend.app.domain.ports"` | Sin error |

---

### 4. Inyección de Dependencias (deps.py)

**Ubicación**: `backend/app/api/deps.py`

#### Descripción

Actualizar deps.py para proporcionar el adaptador de Supabase mediante inyección de dependencias.

#### Requisitos

| ID | Requisito | Tipo |
|----|-----------|------|
| REQ-27 | Crear función `get_supabase_adapter() -> SupabasePort` | Obligatorio |
| REQ-28 | La función retorna una instancia de `SupabaseClientAdapter` | Obligatorio |
| REQ-29 | El adapter usa el cliente de Supabase de `get_supabase()` | Obligatorio |
| REQ-30 | Mantener `get_supabase()` existente para backward compatibility | Recomendado |
| REQ-31 | Tipos usando type hints | Obligatorio |
| REQ-32 | Importar `SupabasePort` y `SupabaseClientAdapter` | Obligatorio |

#### Criterios de Aceptación

| ID | Criterio | Condición |
|----|----------|-----------|
| ACC-13 | Endpoint puede recibir el adaptador | `def endpoint(supabase: SupabasePort = Depends(get_supabase_adapter))` |
| ACC-14 | `get_supabase_adapter()` retorna instancia | No `None` |
| ACC-15 | Tipos pasan mypy | Sin errores |

#### Escenarios de Testing

| Escenario | Input | Output Esperado |
|-----------|-------|-----------------|
| SC-14 | Llamar `get_supabase_adapter()` | Retorna instancia de `SupabaseClientAdapter` |
| SC-15 | Usar como dependencia de FastAPI | Endpoint funciona correctamente |
| SC-16 | Reemplazar con mock en test | Inyección funciona |

---

### 5. Refactorizar ClienteService

**Ubicación**: `backend/app/services/cliente_service.py`

#### Descripción

Actualizar ClienteService para usar el puerto inyectado en lugar de crear su propia conexión.

#### Requisitos

| ID | Requisito | Tipo |
|----|-----------|------|
| REQ-33 | Constructor recibe `SupabasePort` como parámetro | Obligatorio |
| REQ-34 | Eliminar función `get_supabase()` del archivo | Obligatorio |
| REQ-35 | Usar `self.supabase_port` en lugar de `self.supabase` | Obligatorio |
| REQ-36 | Usar métodos del puerto (`get_all`, `get_one`, `insert`, `update`, `delete`) | Obligatorio |
| REQ-37 | Mantener misma interfaz pública (mismos métodos) | Obligatorio |
| REQ-38 | Soportar backwards compatible conClienteService() (sin args) para backward | Recomendado |

#### Criterios de Aceptación

| ID | Criterio | Condición |
|----|----------|-----------|
| ACC-16 | ClienteService recibe el puerto como dependencia | Constructor acepta `supabase_port: SupabasePort` |
| ACC-17 | No crea su propia conexión | Sin `create_client` en el servicio |
| ACC-18 | Endpoints funcionan igual que antes | `/clientes`, `/clientes/{id}`, POST, PUT, DELETE |
| ACC-19 | Tipos pasan mypy | Sin errores |

#### Escenarios de Testing

| Escenario | Input | Output Esperado |
|-----------|-------|-----------------|
| SC-17 | Crear `ClienteService(port)` con mock | Servicio usa el mock |
| SC-18 | `service.get_all(user_id)` con mock | Retorna datos del mock |
| SC-19 | `service.create(data, user_id)` | Llama a `port.insert()` |
| SC-20 | Integrar con endpoint existente | Funciona igual que antes |

---

### 6. Tests para el Nuevo Código

**Ubicación**: `tests/`

#### Descripción

Agregar tests para el adapter y el service refactorizado.

#### Requisitos

| ID | Requisito | Tipo |
|----|-----------|------|
| REQ-39 | Crear `tests/test_supabase_adapter.py` | Obligatorio |
| REQ-40 | Test del método `get_one` con mock de Supabase | Obligatorio |
| REQ-41 | Test del método `get_all` con mock de Supabase | Obligatorio |
| REQ-42 | Test del método `insert` con mock de Supabase | Obligatorio |
| REQ-43 | Test del método `update` con mock de Supabase | Obligatorio |
| REQ-44 | Test del método `delete` con mock de Supabase | Obligatorio |
| REQ-45 | Crear `tests/test_cliente_service.py` | Obligatorio |
| REQ-46 | Test de `get_all` con mock del puerto | Obligatorio |
| REQ-47 | Test de `create` con mock del puerto | Obligatorio |
| REQ-48 | Test de `get_by_id` con mock del puerto | Obligatorio |
| REQ-49 | Coverage del nuevo código > 70% | Obligatorio |
| REQ-50 | Tests pasan con `pytest` | Obligatorio |

#### Criterios de Aceptación

| ID | Criterio | Condición |
|----|----------|-----------|
| ACC-20 | Tests pasan | `pytest tests/ -v` sin fallas |
| ACC-21 | Coverage > 70% | `pytest --cov=backend.app` |
| ACC-22 | Mocks funcionan | Sin llamadas a Supabase real |
| ACC-23 | Tests son mantenibles | Nombres claros, setup simple |

#### Escenarios de Testing

| Escenario | Input | Output Esperado |
|-----------|-------|-----------------|
| SC-21 | `pytest tests/test_supabase_adapter.py` | Todos pasan |
| SC-22 | `pytest tests/test_cliente_service.py` | Todos pasan |
| SC-23 | Coverage report | > 70% en nuevos archivos |
| SC-24 | Test con datos vacíos | Maneja gracefully |

---

## Dependencias

| Dependencia | Versión | Propósito |
|-------------|---------|-----------|
| fastapi | any | API framework |
| supabase | any | Cliente Supabase |
| pytest | any | Testing framework |
| pytest-asyncio | any | Tests async |
| pytest-cov | any | Coverage |

---

## Criterios de Éxito

| ID | Criterio | Métrica |
|----|----------|---------|
| SE-01 | ClienteService usa SupabaseAdapter inyectado | No usa `get_supabase()` directo |
| SE-02 | Endpoints funcionan igual que antes | Tests de integración pasan |
| SE-03 | Tests nuevos pasan | `pytest` 100% verde |
| SE-04 | Código pasa ruff check | `ruff check backend/app` |
| SE-05 | Código pasa mypy | `mypy backend/app` |
| SE-06 | Puerto e implementación documentados | Docstrings en todos los métodos |

---

## Notas Adicionales

- El approach es **Strangler Fig Pattern**: crear nuevo código sin modificar el legacy, refactorizar un servicio como piloto (Cliente), mantener el resto funcionando en paralelo.
- El cambio es backward compatible: el endpoint `/clientes` seguirá funcionando igual después de la refactorización.
- La Fase 2+ migrará los otros 6 módulos (contratos, documentos, etc.).