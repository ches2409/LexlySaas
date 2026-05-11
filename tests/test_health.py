"""Tests for health endpoint"""


def test_health_returns_200(client):
    """Test that /api/v1/health returns 200 status code."""
    response = client.get("/api/v1/health")
    assert response.status_code == 200


def test_health_returns_ok_status(client):
    """Test that /api/v1/health returns ok status."""
    response = client.get("/api/v1/health")
    data = response.json()
    assert data["status"] == "ok"


def test_health_returns_version(client):
    """Test that /api/v1/health returns version."""
    response = client.get("/api/v1/health")
    data = response.json()
    assert "version" in data
    assert data["version"] == "0.1.0"