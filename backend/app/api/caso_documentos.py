"""
API de Documentos de Caso - refactorizado con Arquitectura Hexagonal
"""
from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from typing import Optional

from backend.app.api.deps import get_current_user, get_supabase_adapter
from backend.app.schemas.documento import DocumentoCreate, DocumentoUpdate
from backend.app.services.documento_service import DocumentoService
from backend.app.domain.ports.supabase_port import SupabasePort

router = APIRouter()


def get_documento_service(supabase: SupabasePort = Depends(get_supabase_adapter)) -> DocumentoService:
    """Factory para crear DocumentoService con inyección de dependencias."""
    return DocumentoService(supabase)


@router.get("/caso-documentos")
async def get_documentos(
    caso_id: Optional[str] = None,
    current_user: dict = Depends(get_current_user),
    service: DocumentoService = Depends(get_documento_service)
):
    """Obtener documentos, opcionalmente filtrados por caso_id"""
    user_id = current_user.get("sub")
    documentos = await service.get_all(caso_id=caso_id, user_id=user_id)
    return JSONResponse(content=documentos)


@router.post("/caso-documentos")
async def create_documento(
    doc: DocumentoCreate,
    current_user: dict = Depends(get_current_user),
    service: DocumentoService = Depends(get_documento_service)
):
    """Crear documento"""
    user_id = current_user.get("sub")
    try:
        nuevo = await service.create(doc.model_dump(), user_id)
        return JSONResponse(content=nuevo)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/caso-documentos/{doc_id}")
async def update_documento(
    doc_id: str,
    doc: DocumentoUpdate,
    current_user: dict = Depends(get_current_user),
    service: DocumentoService = Depends(get_documento_service)
):
    """Actualizar documento"""
    user_id = current_user.get("sub")
    actualizado = await service.update(doc_id, doc.model_dump(exclude_unset=True), user_id)
    if not actualizado:
        raise HTTPException(status_code=404, detail="Documento no encontrado")
    return JSONResponse(content=actualizado)


@router.delete("/caso-documentos/{doc_id}")
async def delete_documento(
    doc_id: str,
    current_user: dict = Depends(get_current_user),
    service: DocumentoService = Depends(get_documento_service)
):
    """Eliminar documento"""
    user_id = current_user.get("sub")
    result = await service.delete(doc_id, user_id)
    if not result:
        raise HTTPException(status_code=404, detail="Documento no encontrado")
    return JSONResponse(content={"success": True, "message": "Documento eliminado"})