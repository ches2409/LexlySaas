"""
Debug endpoints - Test Supabase connection
"""
from fastapi import APIRouter
from supabase import create_client
import os
from dotenv import load_dotenv

load_dotenv("/media/chesdevos/CHESDEVS1/proyectos/lexlySaas/.env")

router = APIRouter()


@router.get("/debug/test")
async def test_connection():
    """Test Supabase connection"""
    try:
        supabase_url = os.getenv("SUPABASE_URL")
        supabase_key = os.getenv("SUPABASE_ANON_KEY")
        supabase = create_client(supabase_url, supabase_key)

        # Test casos
        casos = supabase.table("casos").select("id,numero_expediente").limit(3).execute()

        # Test clientes
        clientes = supabase.table("clientes").select("id,nombre,apellido").limit(3).execute()

        return {
            "status": "ok",
            "supabase_url": supabase_url,
            "casos_count": len(casos.data),
            "clientes_count": len(clientes.data),
            "casos": casos.data,
            "clientes": clientes.data
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }