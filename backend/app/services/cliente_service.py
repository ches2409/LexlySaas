"""
Cliente Service - refactorizado con Arquitectura Hexagonal
"""
from typing import List, Optional, Dict, Any

from backend.app.domain.ports.supabase_port import SupabasePort


def get_supabase() -> "SupabasePort":
    """Obtener cliente de Supabase (para backward compatibility)"""
    import os
    from dotenv import load_dotenv
    load_dotenv("/media/chesdevos/CHESDEVS1/proyectos/lexlySaas/.env")
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_ANON_KEY")
    from supabase import create_client
    from backend.app.infrastructure.adapters.supabase_adapter import SupabaseClientAdapter
    client = create_client(supabase_url, supabase_key)
    return SupabaseClientAdapter(client)


class ClienteService:
    """Servicio de Cliente usando inyección de dependencias (Arquitectura Hexagonal)"""

    def __init__(self, supabase: Optional[SupabasePort] = None):
        self.supabase = supabase if supabase is not None else get_supabase()

    async def get_all(self, user_id: str) -> List[Dict[str, Any]]:
        """Obtiene todos los clientes del usuario"""
        # Por ahora retorna todos los clientes
        # TODO: filtrar por user_id
        response = self.supabase.get_all("clientes", {}, limit=1000, offset=0)
        # Ordenar por apellido en Python ya que el puerto no soporta order by
        return sorted(response, key=lambda x: x.get("apellido", ""))

    async def get_by_id(self, cliente_id: str, user_id: str) -> Optional[Dict[str, Any]]:
        """Obtiene un cliente por ID"""
        # Por ahora retorna el cliente sin verificar user_id
        # TODO: verificar que el cliente pertenece al usuario
        return self.supabase.get_one("clientes", {"id": cliente_id})

    async def create(self, data: Dict[str, Any], user_id: str) -> Dict[str, Any]:
        """Crea un nuevo cliente"""
        cliente_data = {
            "user_id": user_id,
            "nombre": data.get("nombre"),
            "apellido": data.get("apellido"),
            "email": data.get("email"),
            "telefono": data.get("telefono"),
            "pais_origen": data.get("pais_origen"),
            "numero_pasaporte": data.get("numero_pasaporte"),
            "estado": "activo"
        }
        return self.supabase.insert("clientes", cliente_data)

    async def update(self, cliente_id: str, data: Dict[str, Any], user_id: str) -> Optional[Dict[str, Any]]:
        """Actualiza un cliente existente"""
        cliente = await self.get_by_id(cliente_id, user_id)
        if not cliente:
            return None

        update_data = {k: v for k, v in data.items() if v is not None and k not in ['id', 'user_id', 'created_at']}
        return self.supabase.update("clientes", {"id": cliente_id}, update_data)

    async def delete(self, cliente_id: str, user_id: str) -> bool:
        """Elimina un cliente"""
        cliente = await self.get_by_id(cliente_id, user_id)
        if not cliente:
            return False

        return self.supabase.delete("clientes", {"id": cliente_id})