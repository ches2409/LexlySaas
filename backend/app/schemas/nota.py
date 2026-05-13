"""Schemas de Nota - Pydantic Models"""
from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class NotaBase(BaseModel):
    """Base fields for Nota"""
    caso_id: str
    contenido: str
    tipo: Optional[str] = "interna"


class NotaCreate(NotaBase):
    """Schema para crear Nota"""
    pass


class NotaUpdate(BaseModel):
    """Schema para actualizar Nota - todos opcionales"""
    contenido: Optional[str] = None
    tipo: Optional[str] = None


class NotaResponse(NotaBase):
    """Schema para respuesta de Nota"""
    id: str
    created_by: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True