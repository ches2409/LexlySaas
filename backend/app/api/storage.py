"""Endpoints para gestión de archivos/storage"""
from fastapi import APIRouter, HTTPException, Depends, UploadFile, File, Form
from fastapi.responses import JSONResponse
from typing import Optional
import uuid

from backend.app.api.deps import get_current_user, get_storage_adapter
from backend.app.domain.ports.storage_port import StoragePort

router = APIRouter()

# Límites de tamaño (50MB para documentos, 5MB para avatares)
MAX_DOCUMENT_SIZE = 50 * 1024 * 1024  # 50MB
MAX_AVATAR_SIZE = 5 * 1024 * 1024  # 5MB

# Tipos MIME permitidos
ALLOWED_DOCUMENT_TYPES = [
    "application/pdf",
    "image/jpeg",
    "image/png",
    "image/webp",
    "application/msword",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
]
ALLOWED_AVATAR_TYPES = ["image/jpeg", "image/png", "image/webp"]


def get_documento_service(storage: StoragePort = Depends(get_storage_adapter)):
    """Factory para crear el servicio de documentos con storage"""
    return storage


@router.post("/upload/documento")
async def upload_documento(
    file: UploadFile = File(...),
    caso_id: str = Form(...),
    categoria: str = Form(...),
    current_user: dict = Depends(get_current_user),
    storage: StoragePort = Depends(get_documento_service)
):
    """Subir documento a un caso"""
    user_id = current_user.get("sub")
    
    # Validar tamaño
    file.file.seek(0, 2)  # Ir al final
    size = file.file.tell()
    file.file.seek(0)  # Volver al inicio
    
    if size > MAX_DOCUMENT_SIZE:
        raise HTTPException(
            status_code=400,
            detail=f"El archivo excede el límite de 50MB"
        )
    
    # Validar tipo MIME
    if file.content_type not in ALLOWED_DOCUMENT_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f"Tipo de archivo no permitido: {file.content_type}"
        )
    
    # Generar path único: user_id/caso_id/nombre_archivo
    extension = file.filename.split(".")[-1] if "." in file.filename else ""
    unique_name = f"{uuid.uuid4()}.{extension}" if extension else str(uuid.uuid4())
    file_path = f"{user_id}/{caso_id}/{unique_name}"
    
    # Leer contenido
    content = await file.read()
    
    # Metadata
    metadata = {
        "user_id": user_id,
        "caso_id": caso_id,
        "categoria": categoria,
        "original_name": file.filename,
        "size": size,
        "mime_type": file.content_type
    }
    
    try:
        # Subir a storage
        result = storage.upload_file(
            bucket="documentos-casos",
            file_path=file_path,
            file_content=content,
            content_type=file.content_type,
            metadata=metadata
        )
        
        return JSONResponse(content={
            "success": True,
            "path": result["path"],
            "url": result["url"],
            "size": size,
            "content_type": file.content_type,
            "original_name": file.filename
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al subir archivo: {str(e)}")


@router.post("/upload/avatar")
async def upload_avatar(
    file: UploadFile = File(...),
    current_user: dict = Depends(get_current_user),
    storage: StoragePort = Depends(get_documento_service)
):
    """Subir avatar de usuario"""
    user_id = current_user.get("sub")
    
    # Validar tamaño
    file.file.seek(0, 2)
    size = file.file.tell()
    file.file.seek(0)
    
    if size > MAX_AVATAR_SIZE:
        raise HTTPException(
            status_code=400,
            detail=f"El archivo excede el límite de 5MB"
        )
    
    # Validar tipo MIME
    if file.content_type not in ALLOWED_AVATAR_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f"Tipo de imagen no permitido: {file.content_type}"
        )
    
    # Generar path único
    extension = file.filename.split(".")[-1] if "." in file.filename else "jpg"
    file_path = f"{user_id}/avatar.{extension}"
    
    # Leer contenido
    content = await file.read()
    
    # Metadata
    metadata = {
        "user_id": user_id
    }
    
    try:
        result = storage.upload_file(
            bucket="avatares",
            file_path=file_path,
            file_content=content,
            content_type=file.content_type,
            metadata=metadata
        )
        
        return JSONResponse(content={
            "success": True,
            "path": result["path"],
            "url": result["url"]
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al subir avatar: {str(e)}")


@router.delete("/delete/{bucket}/{file_path:path}")
async def delete_file(
    bucket: str,
    file_path: str,
    current_user: dict = Depends(get_current_user),
    storage: StoragePort = Depends(get_documento_service)
):
    """Eliminar archivo"""
    # Validar bucket
    if bucket not in ["documentos-casos", "avatares"]:
        raise HTTPException(status_code=400, detail="Bucket no válido")
    
    try:
        success = storage.delete_file(bucket, file_path)
        if success:
            return JSONResponse(content={
                "success": True,
                "message": "Archivo eliminado"
            })
        else:
            raise HTTPException(status_code=404, detail="Archivo no encontrado")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al eliminar: {str(e)}")


@router.get("/signed-url/{bucket}/{file_path:path}")
async def get_signed_url(
    bucket: str,
    file_path: str,
    expires_in: int = 3600,
    current_user: dict = Depends(get_current_user),
    storage: StoragePort = Depends(get_documento_service)
):
    """Obtener URL firmada para acceso temporal"""
    if bucket not in ["documentos-casos", "avatares"]:
        raise HTTPException(status_code=400, detail="Bucket no válido")
    
    try:
        url = storage.get_signed_url(bucket, file_path, expires_in)
        return JSONResponse(content={
            "url": url,
            "expires_in": expires_in
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@router.get("/list/{bucket}")
async def list_files(
    bucket: str,
    path: Optional[str] = None,
    current_user: dict = Depends(get_current_user),
    storage: StoragePort = Depends(get_documento_service)
):
    """Listar archivos en bucket"""
    if bucket not in ["documentos-casos", "avatares"]:
        raise HTTPException(status_code=400, detail="Bucket no válido")
    
    try:
        files = storage.list_files(bucket, path)
        return JSONResponse(content={"files": files})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")