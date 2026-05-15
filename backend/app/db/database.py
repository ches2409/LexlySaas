"""
Configuración de base de datos con SQLModel + asyncpg
"""
from sqlmodel import SQLModel, create_engine, Session
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv("/media/chesdevos/CHESDEVS1/proyectos/lexlySaas/.env")

# URL de PostgreSQL de Supabase
DATABASE_URL = os.getenv("DATABASE_URL", "")

# Convertir a async URL (asyncpg necesita postgresql+asyncpg://)
if DATABASE_URL.startswith("postgresql://"):
    ASYNC_DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://")
else:
    ASYNC_DATABASE_URL = DATABASE_URL

# Engine asíncrono
if ASYNC_DATABASE_URL:
    engine = create_async_engine(ASYNC_DATABASE_URL, echo=False, future=True)
    
    async_session = sessionmaker(
        engine, 
        class_=AsyncSession, 
        expire_on_commit=False
    )
else:
    engine = None
    async_session = None

async def get_session() -> AsyncSession:
    """Dependency para obtener sesión de DB en endpoints"""
    if not async_session:
        raise RuntimeError("Database not configured")
    async with async_session() as session:
        yield session


def get_session_sync():
    """Obtener sesión sincrónica para scripts"""
    if not async_session:
        raise RuntimeError("Database not configured")
    return async_session()

async def create_db_and_tables():
    """Crear tablas (para desarrollo/testing)"""
    if not engine:
        return
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

# Exportar
__all__ = [
    "SQLModel", 
    "Session", 
    "get_session", 
    "create_db_and_tables", 
    "engine",
    "AsyncSession"
]