"""
Cita Service - refactorizado con Arquitectura Hexagonal
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


class CitaService:
    """Servicio de Cita usando inyección de dependencias (Arquitectura Hexagonal)"""

    def __init__(self, supabase: Optional[SupabasePort] = None):
        self.supabase = supabase if supabase is not None else get_supabase()

    async def get_all(self, caso_id: Optional[str] = None, user_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """Obtiene citas, opcionalmente filtradas por caso_id"""
        if caso_id:
            citas = self.supabase.get_all("citas", {"caso_id": caso_id}, limit=1000, offset=0)
        else:
            citas = self.supabase.get_all("citas", {}, limit=1000, offset=0)
        # Ordenar por fecha_hora desc
        return sorted(citas, key=lambda x: x.get("fecha_hora", ""), reverse=True)

    async def get_by_id(self, cita_id: str, user_id: str) -> Optional[Dict[str, Any]]:
        """Obtiene una cita por ID"""
        return self.supabase.get_one("citas", {"id": cita_id})

    async def create(self, data: Dict[str, Any], user_id: str) -> Dict[str, Any]:
        """Crea una nueva cita"""
        cita_data = {
            "caso_id": data.get("caso_id"),
            "cliente_id": data.get("cliente_id"),
            "titulo": data.get("titulo"),
            "descripcion": data.get("descripcion"),
            "fecha_hora": data.get("fecha_hora"),
            "duracion_minutos": data.get("duracion_minutos", 60),
            "tipo": data.get("tipo", "presencial"),
            "ubicacion": data.get("ubicacion"),
            "estado": data.get("estado", "programada"),
            "created_by": user_id,
        }
        return self.supabase.insert("citas", cita_data)

    async def update(self, cita_id: str, data: Dict[str, Any], user_id: str) -> Optional[Dict[str, Any]]:
        """Actualiza una cita existente"""
        cita = await self.get_by_id(cita_id, user_id)
        if not cita:
            return None

        update_data = {k: v for k, v in data.items() if v is not None and k not in ['id', 'created_by', 'created_at']}
        return self.supabase.update("citas", {"id": cita_id}, update_data)

    async def delete(self, cita_id: str, user_id: str) -> bool:
        """Elimina una cita"""
        cita = await self.get_by_id(cita_id, user_id)
        if not cita:
            return False

        return self.supabase.delete("citas", {"id": cita_id})