"""
Endpoints de Casos - refactorizado con Arquitectura Hexagonal
"""
from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from typing import Optional

from backend.app.api.deps import get_current_user, get_supabase_adapter
from backend.app.schemas.caso import CasoCreate, CasoUpdate
from backend.app.services.caso_service import CasoService
from backend.app.domain.ports.supabase_port import SupabasePort

router = APIRouter()


def get_caso_service(supabase: SupabasePort = Depends(get_supabase_adapter)) -> CasoService:
    """Factory para crear CasoService con inyección de dependencias."""
    return CasoService(supabase)


@router.get("/casos")
async def get_casos(
    current_user: dict = Depends(get_current_user),
    service: CasoService = Depends(get_caso_service)
):
    user_id = current_user.get("sub")
    casos = await service.get_all(user_id)
    return JSONResponse(content=casos)


@router.get("/casos/{caso_id}")
async def get_caso(
    caso_id: str,
    current_user: dict = Depends(get_current_user),
    service: CasoService = Depends(get_caso_service)
):
    user_id = current_user.get("sub")
    caso = await service.get_by_id(caso_id, user_id)
    if not caso:
        raise HTTPException(status_code=404, detail="Caso no encontrado")
    return JSONResponse(content=caso)


@router.post("/casos")
async def create_caso(
    caso: CasoCreate,
    current_user: dict = Depends(get_current_user),
    service: CasoService = Depends(get_caso_service)
):
    user_id = current_user.get("sub")
    try:
        nuevo = await service.create(caso.model_dump(), user_id)
        return JSONResponse(content=nuevo)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/casos/{caso_id}")
async def update_caso(
    caso_id: str,
    caso: CasoUpdate,
    current_user: dict = Depends(get_current_user),
    service: CasoService = Depends(get_caso_service)
):
    user_id = current_user.get("sub")
    actualizado = await service.update(caso_id, caso.model_dump(exclude_unset=True), user_id)
    if not actualizado:
        raise HTTPException(status_code=404, detail="Caso no encontrado")
    return JSONResponse(content=actualizado)


@router.delete("/casos/{caso_id}")
async def delete_caso(
    caso_id: str,
    current_user: dict = Depends(get_current_user),
    service: CasoService = Depends(get_caso_service)
):
    user_id = current_user.get("sub")
    result = await service.delete(caso_id, user_id)
    if not result:
        raise HTTPException(status_code=404, detail="Caso no encontrado")
    return JSONResponse(content={"success": True, "message": "Caso eliminado"})


@router.get("/casos-by-cliente/{cliente_id}")
async def get_casos_by_cliente(
    cliente_id: str,
    current_user: dict = Depends(get_current_user),
    service: CasoService = Depends(get_caso_service)
):
    user_id = current_user.get("sub")
    casos = await service.get_by_cliente(cliente_id, user_id)
    return JSONResponse(content=casos)