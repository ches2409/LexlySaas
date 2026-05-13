"""Schemas de Actividad - Pydantic Models"""
from pydantic import BaseModel
from typing import Optional
from datetime import date


class ActividadBase(BaseModel):
    """Base fields for Actividad"""
    caso_id: str
    titulo: str
    tipo: str
    descripcion: Optional[str] = None
    resultado: Optional[str] = None
    fecha_actividad: Optional[date] = None
    proxima_accion: Optional[str] = None


class ActividadCreate(ActividadBase):
    """Schema para crear Actividad"""
    pass


class ActividadUpdate(BaseModel):
    """Schema para actualizar Actividad - todos opcionales"""
    titulo: Optional[str] = None
    tipo: Optional[str] = None
    descripcion: Optional[str] = None
    resultado: Optional[str] = None
    fecha_actividad: Optional[date] = None
    proxima_accion: Optional[str] = None


class ActividadResponse(ActividadBase):
    """Schema para respuesta de Actividad"""
    id: str
    created_at: Optional[date] = None
    updated_at: Optional[date] = None

    class Config:
        from_attributes = True