"""
Pytest fixtures for api-msj tests.
Sets API_MSJ_SECRET and other required env vars so the app loads and auth works in tests.
"""
import os
import pytest
from fastapi.testclient import TestClient

# Set env before app is imported (so Settings() can load)
TEST_API_KEY = "test-secret-key"
REQUIRED_ENV = {
    "API_MSJ_SECRET": TEST_API_KEY,
    "SMTP_HOST": "smtp.test.com",
    "SMTP_USER": "test@test.com",
    "SMTP_PASS": "test",
    "EMAIL_FROM": "test@test.com",
    "WHATSAPP_TOKEN": "test",
    "WHATSAPP_URL": "test",
}
for k, v in REQUIRED_ENV.items():
    os.environ.setdefault(k, v)

from app.main import app  # noqa: E402


@pytest.fixture
def client():
    """Test client for the FastAPI app."""
    return TestClient(app)


@pytest.fixture
def auth_headers():
    """Headers with valid API Key for service-to-service auth."""
    return {"X-API-Key": os.environ.get("API_MSJ_SECRET", TEST_API_KEY)}


@pytest.fixture
def api_v1():
    """API v1 base path."""
    return "/api/v1"
