"""Schemas de Caso - Pydantic Models"""
from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class CasoBase(BaseModel):
    """Base fields para Caso"""
    cliente_id: str
    numero_expediente: Optional[str] = None
    tipo_tramite: str
    observaciones: Optional[str] = None


class CasoCreate(CasoBase):
    """Schema para crear Caso"""
    pass


class CasoUpdate(BaseModel):
    """Schema para actualizar Caso - todos opcionales"""
    numero_expediente: Optional[str] = None
    tipo_tramite: Optional[str] = None
    estado: Optional[str] = None
    observaciones: Optional[str] = None
    fecha_fin: Optional[str] = None


class CasoResponse(CasoBase):
    """Schema para respuesta de Caso"""
    id: str
    estado: str
    fecha_inicio: Optional[str] = None
    fecha_fin: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True