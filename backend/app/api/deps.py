"""Dependencias para autenticación"""
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from supabase import create_client, Client
import os
import jwt
from datetime import timezone
from dotenv import load_dotenv

from backend.app.domain.ports.supabase_port import SupabasePort
from backend.app.infrastructure.adapters.supabase_adapter import SupabaseClientAdapter
from backend.app.domain.ports.storage_port import StoragePort
from backend.app.infrastructure.adapters.storage_adapter import SupabaseStorageAdapter

load_dotenv("/media/chesdevos/CHESDEVS1/proyectos/lexlySaas/.env")

security = HTTPBearer()

def get_supabase() -> Client:
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_ANON_KEY")
    return create_client(supabase_url, supabase_key)


def get_supabase_adapter() -> SupabasePort:
    """Proveedor del adaptador de Supabase para inyección de dependencias."""
    client = get_supabase()
    return SupabaseClientAdapter(client)


def get_storage_adapter() -> StoragePort:
    """Proveedor del adaptador de Storage para inyección de dependencias."""
    client = get_supabase()
    return SupabaseStorageAdapter(client)

def decode_token(token: str) -> dict:
    jwt_secret = os.getenv("JWT_SECRET")
    jwt_algorithm = os.getenv("JWT_ALGORITHM", "HS256")

    try:
        payload = jwt.decode(
            token,
            jwt_secret,
            algorithms=[jwt_algorithm],
            options={"verify_signature": True}
        )
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expirado")
    except jwt.InvalidTokenError as e:
        raise HTTPException(status_code=401, detail=f"Token inválido: {e}")
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Error: {e}")

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:
    token = credentials.credentials
    return decode_token(token)

def require_role(allowed_roles: list):
    async def role_checker(current_user: dict = Depends(get_current_user)) -> dict:
        user_rol = current_user.get("rol")
        if user_rol not in allowed_roles:
            raise HTTPException(status_code=403, detail=f"Acceso denegado")
        return current_user
    return role_checker