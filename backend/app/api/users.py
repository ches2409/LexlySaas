"""
Endpoints de usuarios
Versión protegida - solo usuarios logueados pueden acceder
"""
from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import Response
from supabase import create_client, Client
import os
import json
from dotenv import load_dotenv

# Importar dependencias de autenticación
from backend.app.api.deps import get_current_user, get_supabase

# Cargar .env desde la raíz del proyecto
load_dotenv("/media/chesdevos/CHESDEVS1/proyectos/lexlySaas/.env")

router = APIRouter()

# ============================================================
# ENDPOINTS PÚBLICOS (sin protección)
# ============================================================

@router.get("/users/public")
async def get_users_public():
    """
    Endpoint PÚBLICO - cualquier puede ver
    (solo IDs y nombres, sin datos sensibles)
    """
    supabase = get_supabase()
    response = supabase.table("users").select("id", "nombre", "rol").execute()
    
    return Response(
        content=json.dumps(response.data, indent=2),
        media_type="application/json"
    )

# ============================================================
# ENDPOINTS PROTEGIDOS (requieren token)
# ============================================================

@router.get("/users")
async def get_users(current_user: dict = Depends(get_current_user)):
    """
    Endpoint PROTEGIDO - solo usuarios logueados
    
    Requires: Authorization: Bearer <token>
    Returns: Lista de usuarios SIN password_hash
    """
    # current_user viene del token (verificado automáticamente)
    print(f"Accessing /users as: {current_user.get('nombre')}")
    
    supabase = get_supabase()
    response = supabase.table("users").select("*").execute()
    
    # Filtrar password_hash ANTES de devolver
    users_safe = []
    for user in response.data:
        user_safe = {
            "id": user.get("id"),
            "email": user.get("email"),
            "nombre": user.get("nombre"),
            "rol": user.get("rol"),
            "activo": user.get("activo"),
            "created_at": user.get("created_at"),
            "updated_at": user.get("updated_at")
        }
        users_safe.append(user_safe)
    
    return Response(
        content=json.dumps(users_safe, indent=2),
        media_type="application/json"
    )

@router.get("/users/{user_id}")
async def get_user(user_id: str, current_user: dict = Depends(get_current_user)):
    """
    Endpoint PROTEGIDO - solo usuarios logueados
    
    Args:
        user_id: ID del usuario a buscar
        current_user: Usuario actual (del token)
    """
    supabase = get_supabase()
    response = supabase.table("users").select("*").eq("id", user_id).execute()
    
    if not response.data:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    user = response.data[0]
    
    # Filtrar password_hash
    user_safe = {
        "id": user.get("id"),
        "email": user.get("email"),
        "nombre": user.get("nombre"),
        "rol": user.get("rol"),
        "activo": user.get("activo"),
        "created_at": user.get("created_at"),
        "updated_at": user.get("updated_at")
    }
    
    return Response(
        content=json.dumps(user_safe, indent=2),
        media_type="application/json"
    )

# ============================================================
# EJEMPLO: Endpoint solo para ADMIN
# ============================================================

@router.get("/users-admin")
async def get_users_admin(current_user: dict = Depends(get_current_user)):
    """
    Endpoint solo para ADMIN
    
    Solo usuarios con rol='admin' pueden acceder.
    otros roles reciben: 403 Forbidden
    """
    # Verificar que sea admin
    if current_user.get("rol") != "admin":
        raise HTTPException(
            status_code=403,
            detail="Solo administradores pueden acceder"
        )
    
    supabase = get_supabase()
    response = supabase.table("users").select("*").execute()
    
    # Filtrar password_hash
    users_safe = []
    for user in response.data:
        user_safe.append({
            "id": user.get("id"),
            "email": user.get("email"),
            "nombre": user.get("nombre"),
            "rol": user.get("rol"),
            "activo": user.get("activo"),
            "created_at": user.get("created_at"),
            "updated_at": user.get("updated_at")
        })
    
    return Response(
        content=json.dumps(users_safe, indent=2),
        media_type="application/json"
    )