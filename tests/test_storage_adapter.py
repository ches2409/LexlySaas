"""Tests para el adaptador de Storage"""
import pytest
from unittest.mock import MagicMock

from backend.app.infrastructure.adapters.storage_adapter import SupabaseStorageAdapter


class MockBucket:
    """Mock del bucket de storage"""
    def __init__(self):
        self.files = {}
    
    def upload(self, path, file, options=None):
        self.files[path] = file
        return [{"path": path}]
    
    def download(self, path):
        return self.files.get(path, b"")
    
    def remove(self, paths):
        """Solo elimina si existe, retorna lista vacía si no"""
        result = []
        for path in paths:
            if path in self.files:
                del self.files[path]
                result.append({"path": path})
        return result
    
    def public_url(self, path):
        return f"https://example.supabase.co/storage/v1/object/public/test-bucket/{path}"
    
    def list(self, path=None):
        return [{"name": f} for f in self.files.keys()]
    
    def create_signed_url(self, path, expires_in):
        return f"https://example.supabase.co/signed/{path}?expires={expires_in}"


class MockStorage:
    """Mock del módulo de storage del cliente"""
    def __init__(self):
        self.bucket = MockBucket()
    
    def from_(self, bucket_name):
        return self.bucket


@pytest.fixture
def mock_client():
    """Fixture que provee un cliente mock de Supabase"""
    client = MagicMock()
    client.storage = MockStorage()
    return client


@pytest.fixture
def adapter(mock_client):
    """Fixture que provee el adaptador con cliente mock"""
    return SupabaseStorageAdapter(mock_client)


def test_upload_file_creates_file(adapter, mock_client):
    """Test que upload_file crea el archivo correctamente"""
    content = b"Test file content"
    
    result = adapter.upload_file(
        bucket="test-bucket",
        file_path="test/file.txt",
        file_content=content,
        content_type="text/plain",
        metadata={"test": "metadata"}
    )
    
    assert "path" in result
    assert "url" in result
    assert "bucket" in result
    assert result["path"] == "test/file.txt"


def test_download_file_returns_content(adapter, mock_client):
    """Test que download_file retorna el contenido"""
    mock_client.storage.bucket.files["test/file.txt"] = b"Test content"
    
    result = adapter.download_file("test-bucket", "test/file.txt")
    
    assert result == b"Test content"


def test_download_file_returns_empty_for_missing(adapter, mock_client):
    """Test que download_file retorna vacío para archivos no encontrados"""
    result = adapter.download_file("test-bucket", "nonexistent/file.txt")
    
    assert result == b""


def test_delete_file_removes_file(adapter, mock_client):
    """Test que delete_file elimina el archivo"""
    mock_client.storage.bucket.files["test/file.txt"] = b"Test content"
    
    result = adapter.delete_file("test-bucket", "test/file.txt")
    
    assert result is True
    assert "test/file.txt" not in mock_client.storage.bucket.files


def test_delete_file_returns_false_for_missing(adapter, mock_client):
    """Test que delete_file retorna False para archivos no encontrados"""
    result = adapter.delete_file("test-bucket", "nonexistent/file.txt")
    
    assert result is False


def test_get_public_url_returns_url(adapter, mock_client):
    """Test que get_public_url retorna la URL correcta"""
    result = adapter.get_public_url("test-bucket", "test/file.txt")
    
    assert "https://" in result
    assert "test/file.txt" in result


def test_list_files_returns_file_list(adapter, mock_client):
    """Test que list_files retorna la lista de archivos"""
    mock_client.storage.bucket.files = {
        "file1.txt": b"content1",
        "file2.txt": b"content2"
    }
    
    result = adapter.list_files("test-bucket")
    
    assert len(result) == 2
    assert all("name" in f for f in result)


def test_list_files_empty_for_empty_bucket(adapter, mock_client):
    """Test que list_files retorna lista vacía para bucket vacío"""
    mock_client.storage.bucket.files = {}
    
    result = adapter.list_files("test-bucket")
    
    assert result == []


def test_upload_without_path_generates_uuid(adapter, mock_client):
    """Test que upload sin path genera UUID automáticamente"""
    content = b"Test content"
    
    result = adapter.upload_file(
        bucket="test-bucket",
        file_path="",  # vacío
        file_content=content,
        content_type="text/plain"
    )
    
    assert result["path"] != ""
    assert len(result["path"]) > 0


def test_get_signed_url_returns_signed_url(adapter, mock_client):
    """Test que get_signed_url retorna URL firmada"""
    result = adapter.get_signed_url("test-bucket", "test/file.txt", expires_in=3600)
    
    assert "signed" in result
    assert "expires" in result