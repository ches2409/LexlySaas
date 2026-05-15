# Exploración: Evolución Arquitectónica de lexlysaas

## Resumen Ejecutivo

Este documento documenta el estado actual del proyecto lexlysaas como base para planificar una evolución arquitectónica completa. El objetivo es pasar del stack actual (FastAPI + Vanilla JS) hacia una infraestructura de calidad con hexagonal architecture y un nuevo frontend en Next.js.

---

## 1. Estado Actual del Proyecto

### 1.1 Backend (FastAPI)

**Estructura encontrada:**

| Módulo | Archivos | Descripción |
|--------|----------|-------------|
| `backend/app/main.py` | 1 archivo | Punto de entrada, configuración FastAPI, CORS, importación de routers |
| `backend/app/api/` | 9 routers | auth, clientes, casos, caso_documentos, caso_actividades, caso_notas, users, health, debug |
| `backend/app/models/` | 3 archivos | cliente.py, caso.py, caso_relations.py (SQLModel) |
| `backend/app/services/` | 2 archivos | cliente_service.py, caso_service.py |
| `backend/app/schemas/` | 2 archivos | cliente.py, caso.py (Pydantic DTOs) |
| `backend/app/db/` | 1 archivo | database.py (SQLModel + asyncpg) |
| `backend/app/api/deps.py` | 1 archivo | Dependencias FastAPI (get_current_user) |

**Análisis de separación de responsabilidades:**

La estructura muestra una embryonal separación en capas (api/services/models/schemas) que sigue un patrón similar a Clean Architecture. Sin embargo, hay problemas fundamentales:

1. **Los servicios usan Supabase Client directamente**: `ClienteService` en `services/cliente_service.py` importa y usa `supabase.create_client()` directamente, sin pasar por los modelos SQLModel definidos en `models/`. Esto rompe la idea de una capa de dominio independiente.

2. **Acoplamiento directo**: Los servicios instancian su propio cliente Supabase internamente (`get_supabase()` definido dentro del service), lo cual dificulta el testing y la inyección de dependencias.

3. **Modelos SQLModel no utilizados**: Los modelos en `models/cliente.py` y `models/caso.py` están definidos pero no se usan realmente en la capa de persistance.

4. **Duplicación de código**: Existe un directorio `/app/` en la raíz con código más básico y otro `/backend/app/` con más código. Esto indica confusión arquitectónica.

**Evaluación de testabilidad:**

- Código medianamente modular a nivel de archivos
- NO testeable sin refactorización por acoplamiento directo a Supabase
- Necesita arquitectura hexagonal (puertos y adaptadores) para ser verdaderamente testeable

### 1.2 Frontend (Vanilla JS)

**Estructura encontrada:**

| Módulo | Archivos | Descripción |
|--------|----------|-------------|
| `frontend/js/app.js` | 1 archivo | Punto de entrada, gestión de token, login |
| `frontend/js/router.js` | 1 archivo | Router SPA simple |
| `frontend/js/api.js` | 1 archivo | Cliente API |
| `frontend/js/config.js` | 1 archivo | Configuración |
| `frontend/js/services/` | 8 archivos | clienteService, casoService, citaService, documentoService, actividadService, casoNotaService, casoActividadService, casoDocumentoService |
| `frontend/js/components/` | 12 componentes | DashboardView, ClientesView, CasosView, CasoDetalleView, CitasView, DocumentosView, CaseAlerts, etc. |
| `frontend/js/ui/` | 2 archivos | modals.js, cards.js |
| `frontend/js/utils/` | 1 archivo | helpers.js |
| `frontend/views/` | 8 vistas | login, dashboard, clientes, casos, caso_detalle, citas, documentos, modals |
| `frontend/css/styles.css` | 1 archivo | Estilos |

**Análisis:**

1. **Vanilla JS con patrones de SPA**: No usa ningún framework (no React, no Vue, no Angular). Todo es JavaScript vanilla con una arquitectura propia de componentes.

2. **Organización interna sólida**: El frontend tiene una buena separación interna:
   - Servicios para lógica de negocio
   - Componentes para views
   - UI para elementos reutilizables
   - Router para navegación

3. **Cantidad de código considerable**: Más de 20 archivos JS con funcionalidad real.

**Esfuerzo de migración a Next.js:**

| Factor |Estimación | Détalles |
|--------|-----------|----------|
| Rewriting de componentes | Alto | Los 12 componentes necesitan reescribirse en React/TS |
| Servicios | Medio-Alto | La lógica de negocio es reutilizable pero requiere adaptación |
| Router | Medio | SPA router actual no es compatible con Next.js App Router |
| Views/HTML | Alto | Las 8 vistas necesitan convertirse a JSX |
| Estilos | Bajo | CSS existente es reutilizable con Tailwind |

**Estimación total de esfuerzo:** 2-3 meses de desarrollo para migración completa.

### 1.3 Testing y Tooling

**Estado actual:**

| Área | Estado | Detalles |
|------|--------|----------|
| `pyproject.toml` | Vacío | Solo tiene project metadata y 2 dependencias básicas |
| pytest | No instalado | No hay framework de testing |
| ruff | No instalado | No hay linter |
| mypy | No instalado | No hay type checking |
| pre-commit | No instalado | No hay hooks |
| tests/ | No existe | No hay directorio de tests |

**Dependencias actuales en pyproject.toml:**

- asyncpg>=0.31.0 (solo lo básico)
- sqlmodel>=0.0.38 (definido pero no usado realmente)

**Makefile:** No existe.

### 1.4 Documentación del Proyecto

**Archivos en docs/:**

| Archivo | Descripción |
|---------|-------------|
| `desarrollo-guia-parte-1.md` (745 líneas) | Guía de desarrollo completa - planeaba FastAPI + PostgreSQL + React + TypeScript |
| `gestion-extranjeria-espana.md` | Documentación del dominio de gestión de extranjería |
| `investigacion-caso-detalle-debug.md` | Investigación de un bug específico |
| `prompt-logo-lexlysaas.md` | Prompt para diseño de logo |
| `desarrollo-guia-parte-1.pdf` | Versión PDF de la guía |

**Hallazgo clave:** La guía de desarrollo (`desarrollo-guia-parte-1.md`) fue creada en Mayo 2026 y planeaba exactamente la evolución que el usuario quiere hacer ahora:
- FastAPI Backend
- PostgreSQL (no Supabase)
- React + TypeScript
- Arquitectura profesional

**Esto indica que ya hubo una planificación previa que nunca se ejecutó.**

---

## 2. Gaps Identificados

### 2.1 Gaps de Infraestructura de Calidad

| Gap | Prioridad | Esfuerzo |
|-----|-----------|----------|
| pytest + tests | Alta | Medio |
| ruff (linting) | Alta | Bajo |
| mypy (types) | Alta | Medio |
| pre-commit hooks | Media | Bajo |
| GitHub Actions CI | Media | Medio |

### 2.2 Gaps de Arquitectura Backend

| Gap | Prioridad | Esfuerzo |
|-----|-----------|----------|
| Arquitectura hexagonal | Alta | Alto |
| Puerto/adaptador para Supabase | Alta | Alto |
| Inyección de dependencias | Alta | Medio |
| Tests de servicios | Alta | Alto |
| Separar modelos de dominio de persistencia | Alta | Medio |
| Resolver dualidad app/ vs backend/ | Alta | Bajo |

### 2.3 Gaps de Frontend

| Gap | Prioridad | Esfuerzo |
|-----|-----------|----------|
| Migración a Next.js | Alta | Alto |
| TypeScript | Alta | Alto |
| Componentes React | Alta | Alto |
| Tailwind CSS | Alta | Medio |
| Rutas/App Router | Alta | Medio |

---

## 3. Recomendaciones

### 3.1 Enfoque de Refactorización Sugerido

**Fase 1: Infraestructura de Calidad (Semana 1)**

No intentar refactorizar código al mismo tiempo que se configura tooling. Primero establecer las bases:

1. Agregar pytest y configuración de tests
2. Agregar ruff con configuración básica
3. Agregar mypy con configuración básica
4. Agregar pre-commit hooks
5. Crear primera suite de tests básicos

**Fase 2: Arquitectura Backend (Semanas 2-4)**

1. **Decidir cuál directorio usar**: `app/` o `backend/app/`. Eliminar duplicación.
2. **Implementar puertos y adaptadores**: Crear abstracción para Supabase
3. **Refactorizar servicios**: Usar inyección de dependencias
4. **Escribir tests de servicios**: Mockear el adaptado de Supabase

**Fase 3: Frontend Nuevo (Semanas 5-12)**

Esto puede hacerse en paralelo con fase 2:

1. Setup Next.js + TypeScript + Tailwind
2. Migrar servicios uno por uno
3. Migrar componentes uno por uno
4. Mantener frontend antiguo funcionando hasta migración completa

### 3.2 Orden Sugerido de Prioridades

| Prioridad | Área | Item |
|----------|------|------|
| 1 | Tooling | Configurar pyproject.toml completo |
| 2 | Backend | Resolver estructura de carpetas (app/ vs backend/) |
| 3 | Backend | Implementar abstracción de puerto para Supabase |
| 4 | Backend | Refactorizar servicios con inyección |
| 5 | Backend | Escribir tests de servicios |
| 6 | Frontend | Setup Next.js + TS + Tailwind |
| 7 | Frontend | Migrar servicios API |
| 8 | Frontend | Migrar componentes |

---

## 4. Riesgos

### 4.1 Riesgos Técnicos

| Riesgo | Probabilidad | Impacto | Mitigación |
|--------|-------------|--------|------------|
| Duplicación de código causando confusión | Alta | Medio | Elegir una estructura y eliminar la otra antes de empezar |
| Guía anterior nunca ejecutada indica posible scope creep | Media | Alto | Definir scope mínimo viable y expandir iterativamente |
| Migración de frontend puede tomar más tiempo estimado | Alta | Alto | Mantener frontend antiguo hasta que nuevo esté completo |
| Perder funcionalidad durante refactorización | Media | Alto | Tests E2E antes de empezar cada fase |

### 4.2 Riesgos de Proyecto

| Riesgo | Probabilidad | Impacto | Mitigación |
|--------|-------------|--------|------------|
| scope expansion infinita | Alta | Alto | Timeline fijo, features fuera van a siguiente iteración |
| Resistencia al cambio de Vanilla JS a Next.js | Media | Medio | Involucrar al equipo en decisiones técnicas |
| Documentación desactualizada vs realidad | Media | Bajo | Mantener docs actualizados con cambios |

---

## 5. Próximos Pasos

### Para elSDD

Antes de iniciar la evolución completa,有必要 crear un SDD (Software Design Document) formal con:

1. **Intent**: Definir exactamente qué se quiere lograr
2. **Scope**: Delimitar alcance (qué incluye y qué NO incluye esta evolución)
3. **Approach**: Elegir approach de refactorización (big bang vs incremental)
4. **Tasks**: Descomponer en tareas ejecutables

### Preguntas de Aclaración

1. ¿Cuál directorio de backend usar: `app/` o `backend/app/`?
2. ¿Se mantiene Supabase como base de datos o se migra a PostgreSQL directo?
3. ¿Timeline propuesto (12 semanas) es realista para el usuario?
4. ¿El frontend antiguo debe mantenerse en producción durante migración o puede desconectarse?

---

## Anexo: Archivos Relevantes del Código

### Backend - main.py (entrada)
```
/media/chesdevos/CHESDEVS1/proyectos/lexlySaas/backend/app/main.py
```

### Backend - servicio ejemplo (ClienteService)
```
/media/chesdevos/CHESDEVS1/proyectos/lexlySaas/backend/app/services/cliente_service.py
```

### Frontend - app.js (entrada)
```
/media/chesdevos/CHESDEVS1/proyectos/lexlySaas/frontend/js/app.js
```

### pyproject.toml (actual)
```
/media/chesdevos/CHESDEVS1/proyectos/lexlySaas/pyproject.toml
```