"""
Endpoint de salud /health
"""
from fastapi import APIRouter
router = APIRouter()
@router.get("/health")
async def health_check():
    """
    Verifica que la API está funcando.
    """
    return {
        "status": "ok",
        "message": "Lexly API running",
        "version": "0.1.0"
    }

