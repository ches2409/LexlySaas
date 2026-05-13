"""Adaptador concreto de Supabase que implementa el puerto abstracto"""
from typing import Any, Optional

from supabase import Client

from backend.app.domain.ports.supabase_port import SupabasePort


class SupabaseClientAdapter(SupabasePort):
    """Adaptador concreto que implementa SupabasePort usando el cliente de Supabase"""

    def __init__(self, client: Client):
        self._client = client

    def get_one(self, table: str, filters: dict[str, Any]) -> Optional[dict[str, Any]]:
        """Retrieve a single record from a table."""
        query = self._client.table(table).select("*")
        for key, value in filters.items():
            query = query.eq(key, value)
        response = query.execute()
        return response.data[0] if response.data else None

    def get_all(
        self,
        table: str,
        filters: dict[str, Any],
        limit: int = 100,
        offset: int = 0,
    ) -> list[dict[str, Any]]:
        """Retrieve multiple records from a table."""
        query = self._client.table(table).select("*")
        for key, value in filters.items():
            query = query.eq(key, value)
        response = query.limit(limit).offset(offset).execute()
        return response.data if response.data else []

    def insert(self, table: str, data: dict[str, Any]) -> dict[str, Any]:
        """Insert a new record into a table."""
        response = self._client.table(table).insert(data).execute()
        return response.data[0] if response.data else {}

    def update(
        self, table: str, filters: dict[str, Any], data: dict[str, Any]
    ) -> dict[str, Any]:
        """Update existing records in a table."""
        query = self._client.table(table).update(data)
        for key, value in filters.items():
            query = query.eq(key, value)
        response = query.execute()
        return response.data[0] if response.data else {}

    def delete(self, table: str, filters: dict[str, Any]) -> bool:
        """Delete records from a table."""
        query = self._client.table(table).delete()
        for key, value in filters.items():
            query = query.eq(key, value)
        response = query.execute()
        return len(response.data) > 0 if response.data else False