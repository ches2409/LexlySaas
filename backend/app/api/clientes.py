"""
Endpoints de Clientes - refactorizado con Arquitectura Hexagonal
"""
from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from typing import Optional

from backend.app.api.deps import get_current_user, get_supabase_adapter
from backend.app.schemas.cliente import ClienteCreate, ClienteUpdate
from backend.app.services.cliente_service import ClienteService
from backend.app.domain.ports.supabase_port import SupabasePort

router = APIRouter()


def get_cliente_service(supabase: SupabasePort = Depends(get_supabase_adapter)) -> ClienteService:
    """Factory para crear ClienteService con inyección de dependencias."""
    return ClienteService(supabase)


@router.get("/clientes")
async def get_clientes(
    current_user: dict = Depends(get_current_user),
    service: ClienteService = Depends(get_cliente_service)
):
    user_id = current_user.get("sub")
    clientes = await service.get_all(user_id)
    return JSONResponse(content=clientes)


@router.get("/clientes/{cliente_id}")
async def get_cliente(
    cliente_id: str,
    current_user: dict = Depends(get_current_user),
    service: ClienteService = Depends(get_cliente_service)
):
    user_id = current_user.get("sub")
    cliente = await service.get_by_id(cliente_id, user_id)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return JSONResponse(content=cliente)


@router.post("/clientes")
async def create_cliente(
    cliente: ClienteCreate,
    current_user: dict = Depends(get_current_user),
    service: ClienteService = Depends(get_cliente_service)
):
    user_id = current_user.get("sub")
    try:
        nuevo = await service.create(cliente.model_dump(), user_id)
        return JSONResponse(content=nuevo)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/clientes/{cliente_id}")
async def update_cliente(
    cliente_id: str,
    cliente: ClienteUpdate,
    current_user: dict = Depends(get_current_user),
    service: ClienteService = Depends(get_cliente_service)
):
    user_id = current_user.get("sub")
    actualizado = await service.update(cliente_id, cliente.model_dump(exclude_unset=True), user_id)
    if not actualizado:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return JSONResponse(content=actualizado)


@router.delete("/clientes/{cliente_id}")
async def delete_cliente(
    cliente_id: str,
    current_user: dict = Depends(get_current_user),
    service: ClienteService = Depends(get_cliente_service)
):
    user_id = current_user.get("sub")
    result = await service.delete(cliente_id, user_id)
    if not result:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return JSONResponse(content={"success": True, "message": "Cliente eliminado"})