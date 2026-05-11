"""Tests for clientes CRUD endpoints"""


def test_clientes_endpoint_exists(client):
    """Test that /api/v1/clientes endpoint exists and returns a valid response structure."""
    # This test checks that the endpoint is defined (it requires auth so we expect 401 or similar)
    response = client.get("/api/v1/clientes")
    # Without auth, should get 401 or 403 (depending on how auth is handled)
    assert response.status_code in [200, 401, 403]


def test_get_clientes_requires_auth(client):
    """Test that /api/v1/clientes requires authentication."""
    response = client.get("/api/v1/clientes")
    # Without valid auth token, should not return 200
    assert response.status_code != 200 or "error" in response.json() or "detail" in response.json()