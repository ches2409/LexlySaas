# SDD Explore: Refactorización a Arquitectura Hexagonal

**Fecha**: 2026-05-11
**Proyecto**: lexlysaas
**Autor**: SDD Executor
**Modo**: Hybrid (Engram + filesystem)

---

## 1. Estado Actual del Backend

### Estructura de carpetas

```
backend/
└── app/
    ├── main.py              # Entry point FastAPI (47 líneas)
    ├── api/                 # Controllers/endpoints
    │   ├── auth.py          # Login/JWT
    │   ├── clientes.py      # CRUD clientes
    │   ├── casos.py         # CRUD casos
    │   ├── caso_documentos.py  # Inline (sin service)
    │   ├── caso_actividades.py # Inline (sin service)
    │   ├── caso_notas.py    # Inline (sin service)
    │   ├── deps.py          # Auth dependencies
    │   ├── users.py
    │   └── health.py
    ├── services/            # Lógica de negocio (débilmente acoplada)
    │   ├── cliente_service.py
    │   └── caso_service.py
    ├── models/              # SQLModel (no usados activamente por los services)
    │   ├── cliente.py
    │   ├── caso.py
    │   └── caso_relations.py
    ├── schemas/             # Pydantic DTOs
    │   ├── cliente.py
    │   └── caso.py
    ├── db/                  # SQLModel + asyncpg config (no usado por services)
    │   └── database.py
    └── core/                # Vacío
```

### Análisis por capa

| Capa | Estado | Observaciones |
|------|--------|---------------|
| **API (Controllers)** | ⚠️ Mixta | `clientes.py` y `casos.py` usan services correctamente. Los otros 3 endpoints (`caso_documentos`, `caso_actividades`, `caso_notas`) usan Supabase directamente inline — sin service. |
| **Services** | 🔴 Acoplado | `ClienteService` y `CasoService` crean su propia instancia de `get_supabase()` internamente. No hay abstracción ni inyección. |
| **Models** | ⚠️ Parcial | SQLModel define la estructura pero los services usan Supabase (Postgres) directamente — los models no se usan activamente. |
| **Schemas** | ✅ Bien | Pydantic V2 con BaseModel limpio. Create/Update/Response separados. |
| **Auth** | ⚠️ Funcional | JWT + Supabase, pero la lógica está embebida en `deps.py` y `auth.py`. `verify_password` es un hardcoded placeholder (línea 46 de `auth.py`). |
| **Testing** | ❌ Ninguno | No hay tests. La arquitectura actual no lo facilita. |

### Patrones detectados

**PROBLEMA CRÍTICO: Duplicación de `get_supabase()`**

```python
# Aparece en:
# 1. services/cliente_service.py (línea 8-16)
# 2. services/caso_service.py (línea 8-16)
# 3. api/deps.py (línea 14-17)
# 4. api/auth.py (línea 21-24)
# 5. api/caso_documentos.py (línea 6)
# 6. api/caso_actividades.py (línea 6)
# 7. api/caso_notas.py (línea 6)
```

Cada lugar hace:
```python
load_dotenv("/media/chesdevos/CHESDEVS1/proyectos/lexlySaas/.env")
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_ANON_KEY")
create_client(supabase_url, supabase_key)
```

**PROBLEMA: Business logic inline en endpoints**

Los archivos `caso_documentos.py`, `caso_actividades.py`, y `caso_notas.py` no tienen service correspondiente. Toda la lógica está en el endpoint:

```python
# api/caso_notas.py — sin separación de concerns
@router.get("/caso-notas")
async def get_notas(...):
    supabase = get_supabase()  # Acoplado directo
    query = supabase.table("caso_notas").select("*")
    result = query.order("created_at", desc=True).execute()
```

---

## 2. Entidades de Dominio Identificadas

| Entidad | Tipo | Status | Relaciones |
|---------|------|--------|------------|
| **Cliente** | Core | Service existente | → Casos (1:N) |
| **Caso** | Core | Service existente | → Cliente (N:1), Documentos, Actividades, Notas, Citas |
| **CasoDocumento** | Relacionada | Inline en endpoint | → Caso (N:1) |
| **CasoActividad** | Relacionada | Inline en endpoint | → Caso (N:1) |
| **CasoNota** | Relacionada | Inline en endpoint | → Caso (N:1) |
| **Cita** | Relacionada | Model existe, sin endpoint | → Caso (N:1), → Cliente (N:1) |
| **User** | Autenticación | Embebido en auth.py | — |

### Modelo relacional implícito

```
Cliente (1) ──────< Caso (N)
  │
  └──< Cita (N)
         │
         └──< CasoActividad (N)
         └──< CasoDocumento (N)
         └──< CasoNota (N)
```

---

## 3. Gaps para Arquitectura Hexagonal

### Lo que existe que podemos reutilizar

| Recurso | Se puede usar como |
|---------|---------------------|
| `models/` (SQLModel) | Base para **entidades de dominio** |
| `schemas/` (Pydantic) | Base para **DTOs de entrada/salida** |
| `services/` existentes | Base para **use cases** (refactorizar) |
| `api/deps.py` (`get_current_user`) | Base para **puerto de autenticación** |

### Lo que falta

| Gap | Descripción | Impacto |
|-----|-------------|---------|
| **No hay puertos (interfaces)** | No existe abstracción `ClienteRepository`, `CasoRepository`, `AuthPort`. Services usan `supabase.table()` directo. | Alto — cambiar de base de datos implica reescribir todo |
| **No hay adapters** | El cliente Supabase se instancia directamente. No hay abstracción `SupabaseAdapter`. | Alto — no se pueden mockear para tests |
| **No hay dependency injection** | `ClienteService()` se instancia `new` en cada endpoint. No hay contenedor DI. | Medio — dificulta testing y configuración |
| **Business logic mezclada** | Validaciones como `user_id` ownership checking mezcladas con queries de Supabase en los services. | Medio — lógica de dominio no testeable aisladamente |
| **Auth embebido** | La lógica de JWT verification está en `deps.py`. No hay `AuthService` o `AuthPort`. | Medio — difícil de cambiar auth provider |
| **Sin tests** | No hay tests unitarios ni de integración. | Crítico — refactorizar sin tests es peligroso |
| **Endpoints duplican lógica** | 3 de 6 archivos de API no usan services. | Bajo-Medio — code smell pero funcional |

### Dependencias actuales (cruzadas)

```
API endpoint
    │
    ▼
Service (crea supabase internamente)
    │
    ▼
Supabase Client (creado con load_dotenv + os.getenv)
```

La dirección de las dependencias es **hacia afuera** (hacia Supabase). En hexagonal deben ir **hacia adentro** (hacia el dominio).

---

## 4. Propuesta de Estructura Hexagonal

### Estructura objetivo

```
backend/src/
├── domain/                    # CAPA MÁS INTERNA — sin dependencias externas
│   ├── entities/             # Entidades puras de dominio
│   │   ├── cliente.py       # ClienteEntity (sin ORM)
│   │   ├── caso.py          # CasoEntity
│   │   ├── documento.py      # CasoDocumentoEntity
│   │   ├── actividad.py     # CasoActividadEntity
│   │   └── nota.py          # CasoNotaEntity
│   ├── value_objects/       # Objetos de valor
│   │   ├── email.py
│   │   ├── telefono.py
│   │   └── expediente.py
│   └── services/            # Lógica de dominio pura (sin I/O)
│       ├── cliente_domain_service.py  # Validaciones, reglas de negocio
│       └── caso_domain_service.py
│
├── application/              # CASOS DE USO — orquesta dominio + puertos
│   ├── ports/               # INTERFACES (Abstract Base Classes)
│   │   ├── cliente_repository.py    # Puerto primario (datos)
│   │   ├── caso_repository.py
│   │   ├── documento_repository.py
│   │   ├── actividad_repository.py
│   │   ├── nota_repository.py
│   │   └── auth_port.py             # Puerto secundario (autenticación)
│   └── use_cases/           # IMPLEMENTACIONES concretas
│       ├── cliente/
│       │   ├── get_all_clientes.py
│       │   ├── get_cliente_by_id.py
│       │   ├── create_cliente.py
│       │   ├── update_cliente.py
│       │   └── delete_cliente.py
│       └── caso/
│           ├── get_all_casos.py
│           ├── create_caso.py
│           └── ...
│
├── infrastructure/           # ADAPTADORES — implementaciones concretas
│   ├── adapters/
│   │   └── supabase_adapter.py  # Cliente Supabase configurado
│   ├── repositories/        # IMPLEMENTACIONES de puertos
│   │   ├── supabase_cliente_repository.py
│   │   ├── supabase_caso_repository.py
│   │   └── ...
│   └── auth/                # Implementaciones de auth
│       └── jwt_auth_adapter.py
│
└── api/                     # ENTRADA — controllers FastAPI
    ├── controllers/
    │   ├── cliente_controller.py
    │   ├── caso_controller.py
    │   └── ...
    ├── schemas/             # DTOs de API (request/response)
    │   ├── cliente.py
    │   └── caso.py
    └── dependencies/        # FastAPI Depends para inyección
        ├── get_supabase_client.py
        ├── get_cliente_repository.py
        └── get_authenticated_user.py
```

### Inversión de dependencias

```
         API Controller
              │
              ▼
        Use Case (aplica puerto)
              │
              ▼
         Port (interface ABC)
              │
              ▼
  Repository Adapter (implementación concreta)
              │
              ▼
        Infrastructure (Supabase)
```

**Regla**: `domain` no conoce a `application`. `application` define puertos que `infrastructure` implementa. `api` depende de `application`.

---

## 5. Enfoques de Refactorización

### Enfoque A: Big Bang (Reescritura completa)

**Descripción**: Reescribir toda la estructura desde cero y migrar endpoint por endpoint.

| Pros | Contras |
|------|---------|
| Estructura limpia desde el inicio | Riesgo alto de romper funcionalidad existente |
| Sin deuda técnica residual | Tiempo prolongado sin deliver value |
| Más fácil de diseñar correctamente | Todo el trabajo en un PR grande |

**Esfuerzo**: Muy alto | **Riesgo**: Alto | **Recomendado para**: proyectos nuevos

---

### Enfoque B: Strangler Fig (Incremental por módulo)

**Descripción**: Migrar módulo por módulo. Cada módulo migrado reemplaza al existente.

```
Fase 1: Migrar Cliente
  - Crear domain/entities/cliente.py
  - Crear application/ports/cliente_repository.py
  - Crear infrastructure/repositories/supabase_cliente_repository.py
  - Crear application/use_cases/cliente/*.py
  - Crear api/controllers/cliente_controller.py (nuevo)
  - Mantener api/clientes.py (viejo) hasta que el nuevo esté verificado

Fase 2: Migrar Caso (con relaciones a Cliente)
  - Mismo patrón

Fase 3: Migrar sub-recursos (Documentos, Actividades, Notas)
  - Primero crear services faltantes
  - Luego extraer a use cases

Fase 4: Auth
  - Extraer AuthPort
  - Crear JwtAuthAdapter
  - Refactorizar deps.py
```

| Pros | Contras |
|------|---------|
| Entrega valor incremental | Requiere mantener dos versiones durante transición |
| Cada módulo es independiente | Sobrecarga temporal en el código |
| Fácil de testear por fase | Necesita estrategia de feature flags |
| Bajo riesgo | Más PRs pero más pequeños |

**Esfuerzo**: Distribuido | **Riesgo**: Bajo | **Recomendado**: ✅ **ESTA ES LA RECOMENDACIÓN**

---

### Enfoque C: Extract-Service Pattern (Mínimo viable)

**Descripción**: El mínimo necesario para hacer testeable sin reescribir toda la estructura.

```
backend/app/
├── domain/              # Mover entities a domain (sin ORM, puras)
├── application/         # Renombrar services → use_cases
│   ├── ports/          # Crear abstracciones mínimas
│   └── use_cases/
├── infrastructure/      # Crear adapters/
└── api/                 # Mantener estructura actual, cambiar inyección
```

| Pros | Contras |
|------|---------|
| Cambio más pequeño | Arquitectura incompleta |
| Permite tests rápidos | deuda técnica residual |
| Rápido de implementar | No aprovecha full hexagonal |

**Esfuerzo**: Bajo | **Riesgo**: Bajo | **Recomendado para**: migración inicial rápida

---

## 6. Recomendación

**Elegir Enfoque B (Strangler Fig)** con las siguientes fases:

### Fase 1: Fundaciones (1-2 sprints)
1. Crear estructura de carpetas hexagonal
2. Definir puertos (`ClienteRepository`, `CasoRepository`, `AuthPort`)
3. Crear `SupabaseAdapter` centralizado (eliminar los 7 `get_supabase()` duplicados)
4. Configurar **Dependency Injection** con FastAPI Depends
5. Escribir tests de smoke para los nuevos puertos

### Fase 2: Cliente (1 sprint)
1. Migrar `ClienteService` → use case + repository
2. Crear `ClienteEntity` (domain layer)
3. Reescribir `api/clientes.py` → controller + use case injection
4. Tests unitarios del use case

### Fase 3: Caso + Relaciones (1-2 sprints)
1. Migrar `CasoService` → use case + repository
2. Crear services faltantes para Documentos, Actividades, Notas
3. Extraer a use cases
4. Reescribir endpoints

### Fase 4: Auth + Polish (1 sprint)
1. Extraer AuthPort
2. Centralizar auth en adapter
3. Cleanup de `api/deps.py`
4. Tests de integración

---

## 7. Riesgos

| Riesgo | Severidad | Mitigación |
|--------|----------|------------|
| **Romper funcionalidad existente** | 🔴 Alta | Tests antes de cada fase. Feature flags. Mantener endpoints old + new en paralelo |
| **Scope creep** | 🔴 Alta | Fijar alcance por fase. No agregar features nuevas durante migración |
| **No hay tests actuales** | 🔴 Alta | Escribir tests de smoke antes de empezar. Usar pytest + pytest-asyncio + respx (mock HTTP) |
| **Trabajo paralelo frontend/backend** | 🟡 Media | El frontend usa los endpoints existentes — mientras no cambie el contrato de API, es seguro |
| **Supabase como única dependencia de storage** | 🟡 Media | Definir `DocumentRepository` abstracto — si en el futuro se usa S3, el adapter cambia nada más |
| **Sobrecarga temporal** | 🟡 Media | Durante transición habrá código "viejo + nuevo" coexistiendo. Limpiar al final de cada fase |

---

## 8. Lo que no cambia (contrato de API)

| Aspecto | ¿Cambia? | Notas |
|---------|----------|-------|
| Rutas FastAPI (`/api/v1/clientes`, etc.) | No | Mantener compatibilidad |
| Schemas Pydantic request/response | No (por ahora) | Los DTOs son responsabilidad de la capa API |
| Autenticación JWT | No (interfaz) | La interfaz `get_current_user` se mantiene. Solo la implementación interna cambia |
| Base de datos (Supabase Postgres) | No | El adapter `SupabaseRepository` lo implementa |

---

## 9. Siguiente paso recomendado

Ejecutar **SDD Proposal** para la fase 1 (Fundaciones):
- Definir scope exacto de las fundaciones
- Diseñar los puertos como interfaces ABC
- Planificar la migración de `get_supabase()` a `SupabaseAdapter`
- Definir estrategia de testing antes de empezar

**Next**: `sdd-propose` para `hexagonal-refactor-phase1`
