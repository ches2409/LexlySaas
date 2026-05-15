"""Schemas de Cliente - Pydantic Models"""
from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ClienteBase(BaseModel):
    """Base fields para Cliente"""
    nombre: str
    apellido: str
    # Identificación
    tipo_identificacion: Optional[str] = None  # DNI, Pasaporte, CI, etc.
    numero_identificacion: Optional[str] = None
    # Datos de contacto
    email: Optional[str] = None
    telefono: Optional[str] = None
    pais_origen: Optional[str] = None
    numero_pasaporte: Optional[str] = None
    observaciones: Optional[str] = None


class ClienteCreate(ClienteBase):
    """Schema para crear Cliente"""
    pass


class ClienteUpdate(BaseModel):
    """Schema para actualizar Cliente - todos opcionales"""
    nombre: Optional[str] = None
    apellido: Optional[str] = None
    tipo_identificacion: Optional[str] = None
    numero_identificacion: Optional[str] = None
    email: Optional[str] = None
    telefono: Optional[str] = None
    pais_origen: Optional[str] = None
    numero_pasaporte: Optional[str] = None
    estado: Optional[str] = None
    observaciones: Optional[str] = None


class ClienteResponse(ClienteBase):
    """Schema para respuesta de Cliente"""
    id: str
    estado: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True