"""Adaptador concreto de Storage que implementa el puerto abstracto usando Supabase"""
import uuid
from typing import Optional, Any

from supabase import Client


class SupabaseStorageAdapter:
    """Adaptador concreto que implementa Storage usando Supabase Storage"""

    def __init__(self, client: Client):
        self._client = client

    def _get_bucket(self, bucket: str) -> Any:
        """Obtener referencia al bucket"""
        return self._client.storage.from_(bucket)

    def upload_file(
        self,
        bucket: str,
        file_path: str,
        file_content: bytes,
        content_type: str,
        metadata: Optional[dict] = None
    ) -> dict[str, str]:
        """Upload a file to Supabase Storage"""
        storage = self._get_bucket(bucket)
        
        # Generar nombre único si no hay path específico
        if not file_path:
            file_path = f"{uuid.uuid4()}"
        
        # Subir archivo
        response = storage.upload(
            path=file_path,
            file=file_content,
            options={
                "contentType": content_type,
                "metadata": metadata or {}
            }
        )
        
        # Obtener URL pública
        public_url = self.get_public_url(bucket, file_path)
        
        return {
            "path": file_path,
            "url": public_url,
            "bucket": bucket
        }

    def download_file(self, bucket: str, file_path: str) -> bytes:
        """Download a file from Supabase Storage"""
        storage = self._get_bucket(bucket)
        return storage.download(path=file_path)

    def delete_file(self, bucket: str, file_path: str) -> bool:
        """Delete a file from Supabase Storage"""
        storage = self._get_bucket(bucket)
        response = storage.remove(paths=[file_path])
        return len(response) > 0

    def get_public_url(self, bucket: str, file_path: str) -> str:
        """Get public URL for a file"""
        storage = self._get_bucket(bucket)
        return storage.public_url(path=file_path)

    def list_files(self, bucket: str, path: Optional[str] = None) -> list[dict]:
        """List files in a bucket or folder"""
        storage = self._get_bucket(bucket)
        return storage.list(path=path) or []

    def get_signed_url(self, bucket: str, file_path: str, expires_in: int = 3600) -> str:
        """Get a signed URL for temporary access"""
        storage = self._get_bucket(bucket)
        return storage.create_signed_url(path=file_path, expires_in=expires_in)