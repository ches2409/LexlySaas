"""
Caso Service - refactorizado con Arquitectura Hexagonal
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


class CasoService:
    """Servicio de Caso usando inyección de dependencias (Arquitectura Hexagonal)"""

    def __init__(self, supabase: Optional[SupabasePort] = None):
        self.supabase = supabase if supabase is not None else get_supabase()

    async def get_all(self, user_id: str) -> List[Dict[str, Any]]:
        """Obtiene todos los casos del usuario"""
        # Por ahora retorna todos los casos
        # TODO: filtrar por user_id
        response = self.supabase.get_all("casos", {}, limit=1000, offset=0)
        # Ordenar por created_at desc en Python
        casos = sorted(response, key=lambda x: x.get("created_at", ""), reverse=True)
        # Agregar progreso si no existe
        for caso in casos:
            if "progreso" not in caso:
                caso["progreso"] = 0
        return casos

    async def get_by_id(self, caso_id: str, user_id: str) -> Optional[Dict[str, Any]]:
        """Obtiene un caso por ID"""
        # Por ahora retornamos el caso sin verificar user_id
        # TODO: verificar que el caso pertenece al usuario
        caso = self.supabase.get_one("casos", {"id": caso_id})
        if caso and "progreso" not in caso:
            caso["progreso"] = 0
        return caso

    async def get_by_cliente(self, cliente_id: str, user_id: str) -> List[Dict[str, Any]]:
        """Obtiene todos los casos de un cliente específico"""
        # Verificar que el cliente pertenece al usuario
        cliente = self.supabase.get_one("clientes", {"id": cliente_id, "user_id": user_id})
        if not cliente:
            return []

        casos = self.supabase.get_all("casos", {"cliente_id": cliente_id}, limit=1000, offset=0)
        # Filtrar por user_id en Python
        casos = [c for c in casos if c.get("user_id") == user_id]
        # Ordenar por created_at desc
        return sorted(casos, key=lambda x: x.get("created_at", ""), reverse=True)

    async def create(self, data: Dict[str, Any], user_id: str) -> Dict[str, Any]:
        """Crea un nuevo caso"""
        # Verificar que el cliente pertenece al usuario
        cliente = self.supabase.get_one("clientes", {"id": data.get("cliente_id"), "user_id": user_id})
        if not cliente:
            raise ValueError("Cliente no encontrado")

        caso_data = {
            "user_id": user_id,
            "cliente_id": data.get("cliente_id"),
            "numero_expediente": data.get("numero_expediente"),
            "tipo_tramite": data.get("tipo_tramite"),
            "observaciones": data.get("observaciones"),
            "estado": "inicial"
        }
        return self.supabase.insert("casos", caso_data)

    async def update(self, caso_id: str, data: Dict[str, Any], user_id: str) -> Optional[Dict[str, Any]]:
        """Actualiza un caso existente"""
        caso = await self.get_by_id(caso_id, user_id)
        if not caso:
            return None

        update_data = {k: v for k, v in data.items() if v is not None and k not in ['id', 'user_id', 'created_at']}
        return self.supabase.update("casos", {"id": caso_id}, update_data)

    async def delete(self, caso_id: str, user_id: str) -> bool:
        """Elimina un caso"""
        caso = await self.get_by_id(caso_id, user_id)
        if not caso:
            return False

        return self.supabase.delete("casos", {"id": caso_id})