"""Schemas de Cita - Pydantic Models"""
from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class CitaBase(BaseModel):
    """Base fields for Cita"""
    caso_id: Optional[str] = None
    cliente_id: Optional[str] = None
    titulo: str
    descripcion: Optional[str] = None
    fecha_hora: datetime
    duracion_minutos: int = 60
    tipo: str = "presencial"
    ubicacion: Optional[str] = None


class CitaCreate(CitaBase):
    """Schema para crear Cita"""
    pass


class CitaUpdate(BaseModel):
    """Schema para actualizar Cita - todos opcionales"""
    titulo: Optional[str] = None
    descripcion: Optional[str] = None
    fecha_hora: Optional[datetime] = None
    duracion_minutos: Optional[int] = None
    tipo: Optional[str] = None
    ubicacion: Optional[str] = None
    estado: Optional[str] = None
    notas: Optional[str] = None


class CitaResponse(CitaBase):
    """Schema para respuesta de Cita"""
    id: str
    estado: Optional[str] = "programada"
    recordatorio_enviado: bool = False
    notas: Optional[str] = None
    created_by: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True