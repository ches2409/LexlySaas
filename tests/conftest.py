"""Pytest configuration and fixtures for lexlysaas tests"""

import os
import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

# Add backend to path
backend_path = Path(__file__).parent.parent / "backend"
sys.path.insert(0, str(backend_path.parent))

# Set test environment variables
os.environ["DATABASE_URL"] = "postgresql://test:test@localhost/test"
os.environ["SUPABASE_URL"] = "https://test.supabase.co"
os.environ["SUPABASE_KEY"] = "test-key"
os.environ["SECRET_KEY"] = "test-secret-key"
os.environ["ALGORITHM"] = "HS256"


@pytest.fixture
def client() -> TestClient:
    """Create a test client for the FastAPI app."""
    from backend.app.main import app

    return TestClient(app)


@pytest.fixture
def auth_headers(client: TestClient) -> dict:
    """Create valid auth headers for testing."""
    # This is a placeholder - in real tests you'd create a real token
    return {"Authorization": "Bearer test-token"}