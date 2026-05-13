"""
API de Citas - refactorizado con Arquitectura Hexagonal
"""
from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from typing import Optional

from backend.app.api.deps import get_current_user, get_supabase_adapter
from backend.app.schemas.cita import CitaCreate, CitaUpdate
from backend.app.services.cita_service import CitaService
from backend.app.domain.ports.supabase_port import SupabasePort

router = APIRouter()


def get_cita_service(supabase: SupabasePort = Depends(get_supabase_adapter)) -> CitaService:
    """Factory para crear CitaService con inyección de dependencias."""
    return CitaService(supabase)


@router.get("/citas")
async def get_citas(
    caso_id: Optional[str] = None,
    current_user: dict = Depends(get_current_user),
    service: CitaService = Depends(get_cita_service)
):
    """Obtener citas, opcionalmente filtradas por caso_id"""
    user_id = current_user.get("sub")
    citas = await service.get_all(caso_id=caso_id, user_id=user_id)
    return JSONResponse(content=citas)


@router.post("/citas")
async def create_cita(
    cita: CitaCreate,
    current_user: dict = Depends(get_current_user),
    service: CitaService = Depends(get_cita_service)
):
    """Crear cita"""
    user_id = current_user.get("sub")
    try:
        nueva = await service.create(cita.model_dump(), user_id)
        return JSONResponse(content=nueva)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/citas/{cita_id}")
async def update_cita(
    cita_id: str,
    cita: CitaUpdate,
    current_user: dict = Depends(get_current_user),
    service: CitaService = Depends(get_cita_service)
):
    """Actualizar cita"""
    user_id = current_user.get("sub")
    actualizado = await service.update(cita_id, cita.model_dump(exclude_unset=True), user_id)
    if not actualizado:
        raise HTTPException(status_code=404, detail="Cita no encontrada")
    return JSONResponse(content=actualizado)


@router.delete("/citas/{cita_id}")
async def delete_cita(
    cita_id: str,
    current_user: dict = Depends(get_current_user),
    service: CitaService = Depends(get_cita_service)
):
    """Eliminar cita"""
    user_id = current_user.get("sub")
    result = await service.delete(cita_id, user_id)
    if not result:
        raise HTTPException(status_code=404, detail="Cita no encontrada")
    return JSONResponse(content={"success": True, "message": "Cita eliminada"})