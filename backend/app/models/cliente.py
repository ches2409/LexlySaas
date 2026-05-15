"""
Modelo Cliente - SQLModel
"""
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, TYPE_CHECKING
from datetime import datetime
import uuid

if TYPE_CHECKING:
    from backend.app.models.caso import Caso


class Cliente(SQLModel, table=True):
    """Tabla de Clientes"""
    __tablename__ = "clientes"

    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)

    # User ownership
    user_id: str = Field(index=True)
    
    # Datos personales
    nombre: str = Field(index=True)
    apellido: str = Field(index=True)
    
    # Identificación
    tipo_identificacion: Optional[str] = Field(default=None, max_length=50)  # DNI, Pasaporte, etc.
    numero_identificacion: Optional[str] = Field(default=None, max_length=50)
    
    # Contacto
    email: Optional[str] = Field(default=None, max_length=255)
    telefono: Optional[str] = Field(default=None, max_length=50)
    
    # Origen
    pais_origen: Optional[str] = Field(default=None, max_length=100)
    numero_pasaporte: Optional[str] = Field(default=None, max_length=50)
    
    # Notas
    observaciones: Optional[str] = Field(default=None)
    
    # Estado y timestamps
    estado: str = Field(default="activo", max_length=50)  # activo, inactivo
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default=None)
    
    # Relación con casos
    casos: list["Caso"] = Relationship(back_populates="cliente")
    class Config:
        json_schema_extra = {
            "example": {
                "nombre": "María",
                "apellido": "González",
                "email": "maria@email.com",
                "telefono": "+34 611 123 456"
            }
        }