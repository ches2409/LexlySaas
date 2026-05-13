"""Tests para el adaptador de Supabase"""
import pytest
from unittest.mock import MagicMock, patch

from backend.app.infrastructure.adapters.supabase_adapter import SupabaseClientAdapter


class MockResponse:
    """Mock de respuesta de Supabase"""
    def __init__(self, data):
        self.data = data


@pytest.fixture
def mock_client():
    """Fixture que provee un cliente mock de Supabase"""
    client = MagicMock()
    return client


@pytest.fixture
def adapter(mock_client):
    """Fixture que provee el adaptador con cliente mock"""
    return SupabaseClientAdapter(mock_client)


def test_get_one_returns_record(adapter, mock_client):
    """Test que get_one retorna el registro cuando existe"""
    mock_client.table.return_value.select.return_value.eq.return_value.execute.return_value = MockResponse([{"id": "1", "nombre": "Test"}])

    result = adapter.get_one("clientes", {"id": "1"})

    assert result == {"id": "1", "nombre": "Test"}
    mock_client.table.assert_called_once_with("clientes")


def test_get_one_returns_none_when_empty(adapter, mock_client):
    """Test que get_one retorna None cuando no hay datos"""
    mock_client.table.return_value.select.return_value.eq.return_value.execute.return_value = MockResponse([])

    result = adapter.get_one("clientes", {"id": "nonexistent"})

    assert result is None


def test_get_all_returns_records(adapter, mock_client):
    """Test que get_all retorna lista de registros"""
    mock_client.table.return_value.select.return_value.eq.return_value.limit.return_value.offset.return_value.execute.return_value = MockResponse([{"id": "1"}, {"id": "2"}])

    result = adapter.get_all("clientes", {"user_id": "123"}, limit=10, offset=0)

    assert len(result) == 2
    assert result[0] == {"id": "1"}
    assert result[1] == {"id": "2"}


def test_get_all_returns_empty_when_no_data(adapter, mock_client):
    """Test que get_all retorna lista vacía cuando no hay datos"""
    mock_client.table.return_value.select.return_value.eq.return_value.limit.return_value.offset.return_value.execute.return_value = MockResponse(None)

    result = adapter.get_all("clientes", {})

    assert result == []


def test_insert_returns_created_record(adapter, mock_client):
    """Test que insert retorna el registro creado"""
    mock_client.table.return_value.insert.return_value.execute.return_value = MockResponse([{"id": "1", "nombre": "Nuevo"}])

    result = adapter.insert("clientes", {"nombre": "Nuevo"})

    assert result == {"id": "1", "nombre": "Nuevo"}


def test_update_returns_updated_record(adapter, mock_client):
    """Test que update retorna el registro actualizado"""
    mock_client.table.return_value.update.return_value.eq.return_value.execute.return_value = MockResponse([{"id": "1", "nombre": "Actualizado"}])

    result = adapter.update("clientes", {"id": "1"}, {"nombre": "Actualizado"})

    assert result == {"id": "1", "nombre": "Actualizado"}


def test_delete_returns_true_when_deleted(adapter, mock_client):
    """Test que delete retorna True cuando elimina"""
    mock_client.table.return_value.delete.return_value.eq.return_value.execute.return_value = MockResponse([{"id": "1"}])

    result = adapter.delete("clientes", {"id": "1"})

    assert result is True


def test_delete_returns_false_when_not_found(adapter, mock_client):
    """Test que delete retorna False cuando no encuentra"""
    mock_client.table.return_value.delete.return_value.eq.return_value.execute.return_value = MockResponse([])

    result = adapter.delete("clientes", {"id": "nonexistent"})

    assert result is False