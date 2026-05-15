"""
Modelo Caso - SQLModel
"""
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from datetime import datetime, date
import uuid


class Caso(SQLModel, table=True):
    """Tabla de Casos"""
    __tablename__ = "casos"

    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)

    # User ownership
    user_id: str = Field(index=True)

    # Relaciones
    cliente_id: str = Field(index=True, foreign_key="clientes.id")
    cliente: Optional["Cliente"] = Relationship(back_populates="casos")
    
    # Expediente
    numero_expediente: Optional[str] = Field(default=None, max_length=50, index=True)
    numero_expediente_oficial: Optional[str] = Field(default=None, max_length=50)
    
    # Tipo de trámite
    tipo_tramite: str = Field(max_length=50)  # ciudadania, residencia, visa, etc.
    tipo_procedimiento: Optional[str] = Field(default=None, max_length=100)
    
    # Estado del expediente
    estado: str = Field(default="inicial", max_length=50)  # inicial, documentacion, presentado, etc.
    estado_extranjeria: Optional[str] = Field(default=None, max_length=50)
    
    # Fechas
    fecha_inicio: Optional[date] = Field(default=None)
    fecha_presentacion: Optional[date] = Field(default=None)
    fecha_resolucion: Optional[date] = Field(default=None)
    
    # Resultado
    resultado: Optional[str] = Field(default=None, max_length=100)
    
    # Progreso
    progreso: int = Field(default=0)  # 0-100
    
    # Notas
    observaciones: Optional[str] = Field(default=None)
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default=None)
    
    class Config:
        json_schema_extra = {
            "example": {
                "cliente_id": "uuid-cliente",
                "numero_expediente": "EXP-2026-001",
                "tipo_tramite": "ciudadania",
                "estado": "inicial",
                "progreso": 0
            }
        }