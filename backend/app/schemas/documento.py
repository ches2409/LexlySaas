"""Schemas de Documento - Pydantic Models"""
from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class DocumentoBase(BaseModel):
    """Base fields para Documento"""
    caso_id: str
    nombre: str
    categoria: str
    estado: Optional[str] = "pendiente"
    archivo_url: Optional[str] = None


class DocumentoCreate(DocumentoBase):
    """Schema para crear Documento"""
    pass


class DocumentoUpdate(BaseModel):
    """Schema para actualizar Documento - todos opcionales"""
    nombre: Optional[str] = None
    categoria: Optional[str] = None
    estado: Optional[str] = None
    archivo_url: Optional[str] = None


class DocumentoResponse(DocumentoBase):
    """Schema para respuesta de Documento"""
    id: str
    created_by: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True