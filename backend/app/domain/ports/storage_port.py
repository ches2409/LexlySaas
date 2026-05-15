"""Puerto abstracto para operaciones de Storage"""
from abc import ABC, abstractmethod
from typing import Optional


class StoragePort(ABC):
    """Puerto abstracto para operaciones de storage"""

    @abstractmethod
    def upload_file(
        self,
        bucket: str,
        file_path: str,
        file_content: bytes,
        content_type: str,
        metadata: Optional[dict] = None
    ) -> dict[str, str]:
        """Upload a file to storage. Returns dict with 'path' and 'url'."""
        ...

    @abstractmethod
    def download_file(self, bucket: str, file_path: str) -> bytes:
        """Download a file from storage. Returns file content."""
        ...

    @abstractmethod
    def delete_file(self, bucket: str, file_path: str) -> bool:
        """Delete a file from storage. Returns True if deleted."""
        ...

    @abstractmethod
    def get_public_url(self, bucket: str, file_path: str) -> str:
        """Get public URL for a file. Only works for public buckets."""
        ...