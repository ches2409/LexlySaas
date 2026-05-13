"""Puerto abstracto para operaciones de Supabase"""
from abc import ABC, abstractmethod
from typing import Any, Optional


class SupabasePort(ABC):
    """Puerto abstracto para operaciones de Supabase"""

    @abstractmethod
    def get_one(self, table: str, filters: dict[str, Any]) -> Optional[dict[str, Any]]:
        """Retrieve a single record. Returns None if not found."""
        ...

    @abstractmethod
    def get_all(
        self,
        table: str,
        filters: dict[str, Any],
        limit: int = 100,
        offset: int = 0,
    ) -> list[dict[str, Any]]:
        """Retrieve multiple records with optional pagination."""
        ...

    @abstractmethod
    def insert(self, table: str, data: dict[str, Any]) -> dict[str, Any]:
        """Insert a record and return it."""
        ...

    @abstractmethod
    def update(
        self, table: str, filters: dict[str, Any], data: dict[str, Any]
    ) -> dict[str, Any]:
        """Update records matching filters and return updated record."""
        ...

    @abstractmethod
    def delete(self, table: str, filters: dict[str, Any]) -> bool:
        """Delete records matching filters. Returns True if any deleted."""
        ...