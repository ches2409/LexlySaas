"""
API de Actividades de Caso - refactorizado con Arquitectura Hexagonal
"""
from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from typing import Optional

from backend.app.api.deps import get_current_user, get_supabase_adapter
from backend.app.schemas.actividad import ActividadCreate, ActividadUpdate
from backend.app.services.actividad_service import ActividadService
from backend.app.domain.ports.supabase_port import SupabasePort

router = APIRouter()


def get_actividad_service(supabase: SupabasePort = Depends(get_supabase_adapter)) -> ActividadService:
    """Factory para crear ActividadService con inyección de dependencias."""
    return ActividadService(supabase)


@router.get("/caso-actividades")
async def get_actividades(
    caso_id: Optional[str] = None,
    current_user: dict = Depends(get_current_user),
    service: ActividadService = Depends(get_actividad_service)
):
    """Obtener actividades, opcionalmente filtradas por caso_id"""
    user_id = current_user.get("sub")
    actividades = await service.get_all(caso_id=caso_id, user_id=user_id)
    return JSONResponse(content=actividades)


@router.post("/caso-actividades")
async def create_actividad(
    act: ActividadCreate,
    current_user: dict = Depends(get_current_user),
    service: ActividadService = Depends(get_actividad_service)
):
    """Crear actividad"""
    user_id = current_user.get("sub")
    try:
        nueva = await service.create(act.model_dump(), user_id)
        return JSONResponse(content=nueva)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/caso-actividades/{act_id}")
async def update_actividad(
    act_id: str,
    act: ActividadUpdate,
    current_user: dict = Depends(get_current_user),
    service: ActividadService = Depends(get_actividad_service)
):
    """Actualizar actividad"""
    user_id = current_user.get("sub")
    actualizado = await service.update(act_id, act.model_dump(exclude_unset=True), user_id)
    if not actualizado:
        raise HTTPException(status_code=404, detail="Actividad no encontrada")
    return JSONResponse(content=actualizado)


@router.delete("/caso-actividades/{act_id}")
async def delete_actividad(
    act_id: str,
    current_user: dict = Depends(get_current_user),
    service: ActividadService = Depends(get_actividad_service)
):
    """Eliminar actividad"""
    user_id = current_user.get("sub")
    result = await service.delete(act_id, user_id)
    if not result:
        raise HTTPException(status_code=404, detail="Actividad no encontrada")
    return JSONResponse(content={"success": True, "message": "Actividad eliminada"})