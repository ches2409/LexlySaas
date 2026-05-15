"""
Endpoints de usuarios
"""

from fastapi import APIRouter, HTTPException
from supabase import create_client, Client
import os
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()

# Crear cliente de Supabase
def get_supabase() -> Client:
    """Crear cliente de Supabase."""
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_KEY")
    return create_client(supabase_url, supabase_key)

@router.get("/users")
async def get_users():
    """
    Obtener todos los usuarios.
    """
    supabase = get_supabase()
    response = supabase.table("users").select("*").execute()
    return response.data

@router.get("/users/{user_id}")
async def get_user(user_id: str):
    """
    Obtener un usuario por ID.
    """
    supabase = get_supabase()
    response = supabase.table("users").select("*").eq("id", user_id).execute()
    
    if not response.data:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    return response.data[0]