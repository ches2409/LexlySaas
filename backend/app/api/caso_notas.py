"""
API de Notas de Caso - refactorizado con Arquitectura Hexagonal
"""
from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from typing import Optional

from backend.app.api.deps import get_current_user, get_supabase_adapter
from backend.app.schemas.nota import NotaCreate, NotaUpdate
from backend.app.services.nota_service import NotaService
from backend.app.domain.ports.supabase_port import SupabasePort

router = APIRouter()


def get_nota_service(supabase: SupabasePort = Depends(get_supabase_adapter)) -> NotaService:
    """Factory para crear NotaService con inyección de dependencias."""
    return NotaService(supabase)


@router.get("/caso-notas")
async def get_notas(
    caso_id: Optional[str] = None,
    current_user: dict = Depends(get_current_user),
    service: NotaService = Depends(get_nota_service)
):
    """Obtener notas, opcionalmente filtradas por caso_id"""
    user_id = current_user.get("sub")
    notas = await service.get_all(caso_id=caso_id, user_id=user_id)
    return JSONResponse(content=notas)


@router.post("/caso-notas")
async def create_nota(
    nota: NotaCreate,
    current_user: dict = Depends(get_current_user),
    service: NotaService = Depends(get_nota_service)
):
    """Crear nota"""
    user_id = current_user.get("sub")
    try:
        nueva = await service.create(nota.model_dump(), user_id)
        return JSONResponse(content=nueva)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/caso-notas/{nota_id}")
async def update_nota(
    nota_id: str,
    nota: NotaUpdate,
    current_user: dict = Depends(get_current_user),
    service: NotaService = Depends(get_nota_service)
):
    """Actualizar nota"""
    user_id = current_user.get("sub")
    actualizado = await service.update(nota_id, nota.model_dump(exclude_unset=True), user_id)
    if not actualizado:
        raise HTTPException(status_code=404, detail="Nota no encontrada")
    return JSONResponse(content=actualizado)


@router.delete("/caso-notas/{nota_id}")
async def delete_nota(
    nota_id: str,
    current_user: dict = Depends(get_current_user),
    service: NotaService = Depends(get_nota_service)
):
    """Eliminar nota"""
    user_id = current_user.get("sub")
    result = await service.delete(nota_id, user_id)
    if not result:
        raise HTTPException(status_code=404, detail="Nota no encontrada")
    return JSONResponse(content={"success": True, "message": "Nota eliminada"})