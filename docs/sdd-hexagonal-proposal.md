# Proposal: Arquitectura Hexagonal - Fase 1 (Fundaciones)

## Intent

Establecer las bases de la arquitectura hexagonal creando abstracciones (puertos) e implementaciones (adaptadores) para la dependencia de Supabase. El objetivo es habilitar inyección de dependencias, mejorar la testabilidad, y eliminar los 7 lugares con `get_supabase()` duplicado en el backend actual.

## Scope

### In Scope
1. **SupabasePort** (Puerto/Interfaz): Crear `backend/app/domain/ports/supabase_port.py` con interfaz abstracta definindo métodos: `get_one()`, `get_all()`, `insert()`, `update()`, `delete()`
2. **SupabaseClientAdapter** (Adaptador): Crear `backend/app/infrastructure/adapters/supabase_adapter.py` implementando la interfaz con el cliente actual de Supabase
3. **Inyección de dependencias**: Crear `backend/app/api/deps.py` con providers para el puerto y actualizar endpoints para depender de la abstracción
4. **Reestructuración inicial**: Crear carpetas `domain/ports` e `infrastructure/adapters`, migrar módulo Cliente como piloto

### Out of Scope
- Migrar los otros 6 módulos (contratos, documentos, etc.) — será Fase 2+
- Reescribir toda la lógica de negocio
- Migrar autenticación completa a hexagonal

## Capabilities

### New Capabilities
- `supabase-port`: Interfaz abstracta para operaciones CRUD sobre Supabase
- `supabase-adapter`: Implementación concreta del puerto usando el cliente actual

### Modified Capabilities
- `cliente-service`: Refactorizado para usar inyección de dependencias en lugar de `get_supabase()` directo

## Approach

**Strangler Fig Pattern ( incremental)**:
1. Crear la interfaz (puerto) primero
2. Implementar el adaptador sin modificar código legacy
3. Agregar inyección de dependencias en `deps.py`
4. Refactorizar solo ClienteService como piloto
5. Mantener el resto del código funcionando en paralelo
6. Agregar tests para el nuevo código antes de expandir

## Affected Areas

| Area | Impact | Description |
|------|--------|-------------|
| `backend/app/domain/ports/` | New | Puerto abstracto para Supabase |
| `backend/app/infrastructure/adapters/` | New | Implementación concreta del adaptador |
| `backend/app/api/deps.py` | New | Proveedores de inyección de dependencias |
| `backend/app/services/cliente_service.py` | Modified | Refactorizado para usar inyección |

## Risks

| Risk | Likelihood | Mitigation |
|------|------------|------------|
| Código nuevo y viejo coexistiendo | High | Documentar claramente qué va dónde |
| Sin tests existentes, sin red de seguridad | High | Agregar tests del adapter antes de expandir |
| Resistencia al cambio en el equipo | Medium | Documentar beneficios y gradualidad |

## Rollback Plan

1. Revertir cambios en `cliente_service.py` para usar `get_supabase()` directo
2. Eliminar carpeta `domain/ports/` e `infrastructure/adapters/`
3. Eliminar `deps.py`
4. Los endpoints seguirán funcionando igual que antes

## Dependencies

- FastAPI instalado (ya existe)
- Supabase client (ya existe)

## Success Criteria

- [ ] ClienteService usa SupabaseAdapter inyectado (no `get_supabase()` directo)
- [ ] Endpoints de `/clientes` funcionan igual que antes
- [ ] Tests nuevos pasan (test del adapter + test del use case)
- [ ] Código pasa ruff check y mypy
- [ ] Puerto e implementación documentados con docstrings