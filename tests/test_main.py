import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_read_root():
    """Test the root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "service" in data
    assert "version" in data
    assert "status" in data
    assert data["status"] == "running"


def test_health_check():
    """Test the health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert data["status"] == "healthy"
    assert "service" in data
    assert "version" in data


def test_docs_endpoint():
    """Test that docs endpoint is accessible."""
    response = client.get("/docs")
    assert response.status_code == 200


def test_redoc_endpoint():
    """Test that redoc endpoint is accessible."""
    response = client.get("/redoc")
    assert response.status_code == 200


def test_process_time_header():
    """Test that process time header is added."""
    response = client.get("/")
    assert "X-Process-Time" in response.headers
    assert float(response.headers["X-Process-Time"]) >= 0
