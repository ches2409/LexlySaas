"""
Documento Service - refactorizado con Arquitectura Hexagonal
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


class DocumentoService:
    """Servicio de Documento usando inyección de dependencias (Arquitectura Hexagonal)"""

    def __init__(self, supabase: Optional[SupabasePort] = None):
        self.supabase = supabase if supabase is not None else get_supabase()

    async def get_all(self, caso_id: Optional[str] = None, user_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """Obtiene documentos, opcionalmente filtrados por caso_id"""
        if caso_id:
            documentos = self.supabase.get_all("caso_documentos", {"caso_id": caso_id}, limit=1000, offset=0)
        else:
            documentos = self.supabase.get_all("caso_documentos", {}, limit=1000, offset=0)
        # Ordenar por created_at desc
        return sorted(documentos, key=lambda x: x.get("created_at", ""), reverse=True)

    async def get_by_id(self, doc_id: str, user_id: str) -> Optional[Dict[str, Any]]:
        """Obtiene un documento por ID"""
        return self.supabase.get_one("caso_documentos", {"id": doc_id})

    async def create(self, data: Dict[str, Any], user_id: str) -> Dict[str, Any]:
        """Crea un nuevo documento"""
        doc_data = {
            "caso_id": data.get("caso_id"),
            "nombre": data.get("nombre"),
            "categoria": data.get("categoria"),
            "estado": data.get("estado", "pendiente"),
            "archivo_url": data.get("archivo_url"),
            "created_by": user_id
        }
        return self.supabase.insert("caso_documentos", doc_data)

    async def update(self, doc_id: str, data: Dict[str, Any], user_id: str) -> Optional[Dict[str, Any]]:
        """Actualiza un documento existente"""
        documento = await self.get_by_id(doc_id, user_id)
        if not documento:
            return None

        update_data = {k: v for k, v in data.items() if v is not None and k not in ['id', 'created_by', 'created_at']}
        return self.supabase.update("caso_documentos", {"id": doc_id}, update_data)

    async def delete(self, doc_id: str, user_id: str) -> bool:
        """Elimina un documento"""
        documento = await self.get_by_id(doc_id, user_id)
        if not documento:
            return False

        return self.supabase.delete("caso_documentos", {"id": doc_id})