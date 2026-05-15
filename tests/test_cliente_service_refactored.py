"""Tests para el servicio de Cliente refactorizado con arquitectura hexagonal"""
import pytest
from unittest.mock import MagicMock

from backend.app.services.cliente_service import ClienteService


@pytest.fixture
def mock_supabase_port():
    """Fixture que provee un puerto mock de Supabase (métodos sync)"""
    port = MagicMock()
    # Los métodos del adapter son sync, no async
    port.get_one = MagicMock(return_value=None)
    port.get_all = MagicMock(return_value=[])
    port.insert = MagicMock(return_value={})
    port.update = MagicMock(return_value={})
    port.delete = MagicMock(return_value=False)
    return port


@pytest.fixture
def service(mock_supabase_port):
    """Fixture que provee el servicio con el puerto inyectado"""
    return ClienteService(supabase=mock_supabase_port)


@pytest.mark.asyncio
async def test_get_all_calls_supabase_get_all(service, mock_supabase_port):
    """Test que get_all llama al método get_all del puerto"""
    mock_supabase_port.get_all.return_value = [
        {"id": "1", "apellido": "García"},
        {"id": "2", "apellido": "López"}
    ]

    result = await service.get_all("user123")

    mock_supabase_port.get_all.assert_called_once_with("clientes", {}, limit=1000, offset=0)
    assert len(result) == 2
    assert result[0]["apellido"] == "García"


@pytest.mark.asyncio
async def test_get_by_id_calls_supabase_get_one(service, mock_supabase_port):
    """Test que get_by_id llama al método get_one del puerto"""
    mock_supabase_port.get_one.return_value = {"id": "1", "nombre": "Juan"}

    result = await service.get_by_id("1", "user123")

    mock_supabase_port.get_one.assert_called_once_with("clientes", {"id": "1"})
    assert result == {"id": "1", "nombre": "Juan"}


@pytest.mark.asyncio
async def test_get_by_id_returns_none_when_not_found(service, mock_supabase_port):
    """Test que get_by_id retorna None cuando no encuentra"""
    mock_supabase_port.get_one.return_value = None

    result = await service.get_by_id("nonexistent", "user123")

    assert result is None


@pytest.mark.asyncio
async def test_create_calls_supabase_insert(service, mock_supabase_port):
    """Test que create llama al método insert del puerto"""
    mock_supabase_port.insert.return_value = {"id": "1", "nombre": "Juan", "apellido": "Pérez"}

    data = {"nombre": "Juan", "apellido": "Pérez", "email": "juan@test.com"}
    result = await service.create(data, "user123")

    mock_supabase_port.insert.assert_called_once()
    call_args = mock_supabase_port.insert.call_args
    assert call_args[0][0] == "clientes"
    assert call_args[0][1]["nombre"] == "Juan"
    assert call_args[0][1]["user_id"] == "user123"


@pytest.mark.asyncio
async def test_update_calls_supabase_update(service, mock_supabase_port):
    """Test que update llama al método update del puerto"""
    mock_supabase_port.get_one.return_value = {"id": "1", "nombre": "Juan"}
    mock_supabase_port.update.return_value = {"id": "1", "nombre": "Juan Actualizado"}

    result = await service.update("1", {"nombre": "Juan Actualizado"}, "user123")

    mock_supabase_port.update.assert_called_once_with("clientes", {"id": "1"}, {"nombre": "Juan Actualizado"})


@pytest.mark.asyncio
async def test_update_returns_none_when_not_found(service, mock_supabase_port):
    """Test que update retorna None cuando no encuentra el cliente"""
    mock_supabase_port.get_one.return_value = None

    result = await service.update("nonexistent", {"nombre": "Nuevo"}, "user123")

    assert result is None


@pytest.mark.asyncio
async def test_delete_calls_supabase_delete(service, mock_supabase_port):
    """Test que delete llama al método delete del puerto"""
    mock_supabase_port.get_one.return_value = {"id": "1"}
    mock_supabase_port.delete.return_value = True

    result = await service.delete("1", "user123")

    mock_supabase_port.delete.assert_called_once_with("clientes", {"id": "1"})
    assert result is True


@pytest.mark.asyncio
async def test_delete_returns_false_when_not_found(service, mock_supabase_port):
    """Test que delete retorna False cuando no encuentra el cliente"""
    mock_supabase_port.get_one.return_value = None

    result = await service.delete("nonexistent", "user123")

    assert result is False


def test_service_accepts_supabase_port_in_constructor(service, mock_supabase_port):
    """Test que el servicio acepta un puerto en el constructor"""
    assert service.supabase is mock_supabase_port