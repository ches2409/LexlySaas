"""
Endpoint de test para verificar conexión SQLModel
"""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.db.database import get_session
from sqlmodel import text

router = APIRouter()


@router.get("/test-db")
async def test_db(session: AsyncSession = Depends(get_session)):
    """Test de conexión a la base de datos"""
    try:
        # Test simple query
        result = await session.execute(text("SELECT 1 as test"))
        row = result.fetchone()
        
        # Obtener tables
        tables_result = await session.execute(text(
            "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'"
        ))
        tables = [r[0] for r in tables_result.fetchall()]
        
        return {
            "status": "ok",
            "message": "Conexión a PostgreSQL exitosa",
            "test_query": row[0],
            "tables": tables
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }


@router.get("/test-models")
async def test_models(session: AsyncSession = Depends(get_session)):
    """Test de models SQLModel"""
    from backend.app.models import Cliente, Caso
    
    try:
        # Obtener count de tablas
        result_clientes = await session.execute(text("SELECT COUNT(*) FROM clientes"))
        count_clientes = result_clientes.scalar()
        
        result_casos = await session.execute(text("SELECT COUNT(*) FROM casos"))
        count_casos = result_casos.scalar()
        
        return {
            "status": "ok",
            "clientes_count": count_clientes,
            "casos_count": count_casos,
            "models_loaded": True
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }