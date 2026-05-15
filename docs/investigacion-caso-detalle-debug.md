# Investigación: Vista de Detalle del Caso - Debug Report

## Problema Inicial

Al hacer click en un caso desde la lista de casos, la vista de detalle no cargaba correctamente y lanzaba error:
```
TypeError: Cannot set properties of null (setting 'textContent')
```

## Síntomas

1. Error 404 al cargar `/caso-documentos`, `/caso-actividades`, `/caso-notas`
2. Elementos del DOM (`detalle-caso-titulo`) no encontrados
3. HTML reemplazado por "Cargando caso..."

## Causas Raíz

### Causa 1: Backend no tenía endpoints
Las 3 tablas existían en Supabase pero el backend Python/FastAPI no tenía las rutas API correspondientes.

**Solución:** Crear 3 nuevos archivos de API:
- `backend/app/api/caso_documentos.py`
- `backend/app/api/caso_actividades.py`
- `backend/app/api/caso_notas.py`

### Causa 2: showLoading() destruía el DOM
La función `showLoading()` en `CasoDetalleView.init()` sobreescribía el HTML de `app-content` con un spinner de carga, destroying el HTML que había cargado `loadView()` anteriormente.

**Flow correcto (antes del bug):**
```
1. router.navigate('caso_detalle', id)
   ↓
2. loadView() carga views/caso_detalle.html
   ↓
3. CasoDetalleView.init(id) → showLoading() SOBRESCRIBE el HTML
   ↓
4. render() busca elementos → NULL (se perdieron)
```

**Flow corrected (después del fix):**
```
1. router.navigate('caso_detalle', id)
   ↓
2. loadView() carga views/caso_detalle.html
   ↓
3. CasoDetalleView.init(id) → SIN showLoading()
   ↓
4. render() encuentra los elementos ✓
```

## Archivos Modificados/Creados

### Backend (Python)
- `backend/app/api/caso_documentos.py` (NUEVO)
- `backend/app/api/caso_actividades.py` (NUEVO)
- `backend/app/api/caso_notas.py` (NUEVO)
- `backend/app/main.py` - registrados los 3 nuevos routers

### Frontend (JavaScript/HTML)
- `frontend/js/router.js` - soporte paraparams en navigate()
- `frontend/js/components/CasoDetalleView.js` - eliminado showLoading()
- `frontend/views/caso_detalle.html` - ya existía
- `frontend/css/styles.css` - estilos para detalle tabs

### Linkeos
- `frontend/js/components/CasosView.js` - fila clickeable → router.navigate('caso_detalle', casoId)
- `frontend/js/components/ClientesView.js` -showClientCases() linkeado al detalle

## Lecciones Aprendidas

1. **No usar showLoading() que reemplace todo el contenido** - destruye el HTML ya cargado
2. **Verificar el flujo asíncrono** - El orden importa: loadView() debe completar ANTES de init()
3. **Agregar logging desde el principio** - aceleró el debugging significativamente

## Pendiente (si hay más trabajo)

- Funcionalidad CRUD completa para documentos, actividades y notas
- Formularios para agregar/editar cada tipo
- Persistencia de cambios a Supabase