"""
Endpoint de Autenticación (Login/Logout)
"""
from fastapi import APIRouter, HTTPException
from fastapi.responses import Response
from supabase import create_client, Client
import os
import json
import bcrypt
import jwt
from datetime import datetime, timedelta, timezone
from pydantic import BaseModel
from dotenv import load_dotenv

# Cargar .env desde la raíz del proyecto
load_dotenv("/media/chesdevos/CHESDEVS1/proyectos/lexlySaas/.env")

router = APIRouter()

# Crear cliente de Supabase
def get_supabase() -> Client:
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_ANON_KEY")
    return create_client(supabase_url, supabase_key)

# ============================================================
# MODELOS DE REQUEST/RESPONSE (Schema)
# ============================================================

class LoginRequest(BaseModel):
    email: str
    password: str

class LoginResponse(BaseModel):
    success: bool
    user: dict | None = None
    token: str | None = None

# ============================================================
# FUNCIONES AUXILIARES
# ============================================================

def verify_password(password: str, password_hash: str) -> bool:
    # TODO: usar bcrypt en producción
    # Por ahora acepta password123 para testing
    return password == "password123"

def create_jwt_token(user_data: dict) -> str:
    jwt_secret = os.getenv("JWT_SECRET")
    jwt_algorithm = os.getenv("JWT_ALGORITHM", "HS256")
    jwt_expiration = int(os.getenv("JWT_EXPIRATION_MINUTES", "1440"))
    
    # Crear payload (datos dentro del token)
    payload = {
        "sub": user_data["id"],
        "email": user_data["email"],
        "nombre": user_data["nombre"],
        "rol": user_data["rol"],
        "exp": datetime.now(timezone.utc) + timedelta(minutes=jwt_expiration)
    }
    
    # Generar token FIRMANDO con la clave secreta
    token = jwt.encode(payload, jwt_secret, algorithm=jwt_algorithm)
    
    return token

# ============================================================
# ENDPOINTS
# ============================================================

@router.post("/login")
async def login(request: LoginRequest):
    # 1️⃣ Obtener cliente de Supabase
    supabase = get_supabase()
    
    # 2️⃣ Buscar usuario por email
    response = supabase.table("users").select("*").eq("email", request.email).execute()
    
    # 3️⃣ Verificar si existe
    if not response.data:
        raise HTTPException(
            status_code=401,
            detail="Email o contraseña incorrectos"
        )
    
    user = response.data[0]
    
    # 4️⃣ Verificar si está activo
    if not user.get("activo", True):
        raise HTTPException(
            status_code=401,
            detail="Usuario inactivo. Contacta al administrador."
        )
    
    # 5️⃣ Verificar contraseña
    if not verify_password(request.password, user["password_hash"]):
        raise HTTPException(
            status_code=401,
            detail="Email o contraseña incorrectos"
        )
    
    # 6️⃣ Generar token JWT
    token = create_jwt_token(user)
    
    # 7️⃣ Devolver respuesta (sin password_hash)
    user_without_password = {
        "id": user["id"],
        "email": user["email"],
        "nombre": user["nombre"],
        "rol": user["rol"],
        "activo": user.get("activo", True),
        "created_at": user.get("created_at")
    }
    
    return LoginResponse(
        success=True,
        user=user_without_password,
        token=token
    )