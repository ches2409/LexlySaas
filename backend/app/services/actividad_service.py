"""
Actividad Service - refactorizado con Arquitectura Hexagonal
"""
from typing import List, Optional, Dict, Any
from datetime import date

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


class ActividadService:
    """Servicio de Actividad usando inyección de dependencias (Arquitectura Hexagonal)"""

    def __init__(self, supabase: Optional[SupabasePort] = None):
        self.supabase = supabase if supabase is not None else get_supabase()

    async def get_all(self, caso_id: Optional[str] = None, user_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """Obtiene actividades, opcionalmente filtradas por caso_id"""
        if caso_id:
            actividades = self.supabase.get_all("caso_actividades", {"caso_id": caso_id}, limit=1000, offset=0)
        else:
            actividades = self.supabase.get_all("caso_actividades", {}, limit=1000, offset=0)
        # Ordenar por fecha_actividad desc
        return sorted(actividades, key=lambda x: x.get("fecha_actividad", ""), reverse=True)

    async def get_by_id(self, act_id: str, user_id: str) -> Optional[Dict[str, Any]]:
        """Obtiene una actividad por ID"""
        return self.supabase.get_one("caso_actividades", {"id": act_id})

    async def create(self, data: Dict[str, Any], user_id: str) -> Dict[str, Any]:
        """Crea una nueva actividad"""
        act_data = {
            "caso_id": data.get("caso_id"),
            "titulo": data.get("titulo"),
            "tipo": data.get("tipo"),
            "descripcion": data.get("descripcion"),
            "resultado": data.get("resultado"),
            "fecha_actividad": str(data.get("fecha_actividad")) if data.get("fecha_actividad") else None,
            "proxima_accion": data.get("proxima_accion"),
        }
        return self.supabase.insert("caso_actividades", act_data)

    async def update(self, act_id: str, data: Dict[str, Any], user_id: str) -> Optional[Dict[str, Any]]:
        """Actualiza una actividad existente"""
        actividad = await self.get_by_id(act_id, user_id)
        if not actividad:
            return None

        update_data = {k: v for k, v in data.items() if v is not None and k not in ['id', 'created_at']}
        if update_data.get("fecha_actividad"):
            update_data["fecha_actividad"] = str(update_data["fecha_actividad"])
        return self.supabase.update("caso_actividades", {"id": act_id}, update_data)

    async def delete(self, act_id: str, user_id: str) -> bool:
        """Elimina una actividad"""
        actividad = await self.get_by_id(act_id, user_id)
        if not actividad:
            return False

        return self.supabase.delete("caso_actividades", {"id": act_id})