"""
Modelos de relación con Caso - SQLModel
"""
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from datetime import datetime, date
import uuid


# ============================================
# CASO DOCUMENTO
# ============================================
class CasoDocumento(SQLModel, table=True):
    """Tabla de Documentos de Caso"""
    __tablename__ = "caso_documentos"
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    caso_id: str = Field(index=True)
    
    # Datos del documento
    nombre: str = Field(max_length=255)
    categoria: str = Field(max_length=100)  # identidad, laboral, economico, etc.
    estado: str = Field(default="pendiente", max_length=50)  # pendiente, entregado, no_aplica
    observaciones: Optional[str] = Field(default=None)
    
    # URL del archivo (si se sube a storage)
    archivo_url: Optional[str] = Field(default=None, max_length=500)
    
    # Metadata
    created_by: Optional[str] = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default=None)


# ============================================
# CASO ACTIVIDAD
# ============================================
class CasoActividad(SQLModel, table=True):
    """Tabla de Actividades de Caso"""
    __tablename__ = "caso_actividades"
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    caso_id: str = Field(index=True)
    
    # Datos de la actividad
    titulo: str = Field(max_length=255)
    tipo: str = Field(max_length=50)  # cita, llamada, email, reunion, presentacion, etc.
    descripcion: Optional[str] = Field(default=None)
    resultado: Optional[str] = Field(default=None)
    
    # Fecha de la actividad
    fecha_actividad: Optional[date] = Field(default=None)
    
    # Próxima acción
    proxima_accion: Optional[str] = Field(default=None)
    
    # Metadata
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default=None)


# ============================================
# CASO NOTA
# ============================================
class CasoNota(SQLModel, table=True):
    """Tabla de Notas de Caso"""
    __tablename__ = "caso_notas"
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    caso_id: str = Field(index=True)
    
    # Contenido
    contenido: str = Field()
    tipo: str = Field(default="interna", max_length=50)  # interna, atencion, soporte, revisor, urgente
    
    # Metadata
    created_by: Optional[str] = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default=None)


# ============================================
# CITA (Nueva)
# ============================================
class Cita(SQLModel, table=True):
    """Tabla de Citas"""
    __tablename__ = "citas"
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    caso_id: Optional[str] = Field(default=None, index=True)
    cliente_id: Optional[str] = Field(default=None, index=True)
    
    # Datos de la cita
    titulo: str = Field(max_length=255)
    descripcion: Optional[str] = Field(default=None)
    fecha_hora: datetime = Field(index=True)
    duracion_minutos: int = Field(default=60)
    
    # Tipo y ubicación
    tipo: str = Field(default="presencial", max_length=50)  # presencial, telefonica, videollamada
    ubicacion: Optional[str] = Field(default=None, max_length=255)
    
    # Estado
    estado: str = Field(default="programada", max_length=50)  # programada, confirmada, completada, cancelada
    recordatorio_enviado: bool = Field(default=False)
    
    # Notas post-cita
    notas: Optional[str] = Field(default=None)
    
    # Metadata
    created_by: Optional[str] = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default=None)