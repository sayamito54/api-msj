import pytest


def test_read_root(client):
    """Test the root endpoint returns welcome message, api_v1 prefix and version."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert data.get("api_v1") == "/api/v1"
    assert "version" in data
    assert data.get("status") == "running"
    assert "service" in data


def test_health_check(client):
    """Test the health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert data["status"] == "healthy"
    assert "service" in data
    assert "version" in data


def test_docs_endpoint(client):
    """Test that docs endpoint is accessible when ENABLE_OPENAPI_DOCS is true."""
    response = client.get("/docs")
    assert response.status_code == 200


def test_redoc_endpoint(client):
    """Test that redoc endpoint is accessible when ENABLE_OPENAPI_DOCS is true."""
    response = client.get("/redoc")
    assert response.status_code == 200


def test_process_time_header(client):
    """Test that process time header is added."""
    response = client.get("/")
    assert "X-Process-Time" in response.headers
    assert float(response.headers["X-Process-Time"]) >= 0


# --- API v1 protected endpoints: require API Key ---


def test_email_send_requires_auth(client, api_v1):
    """Without API Key, POST /api/v1/email/send returns 401."""
    response = client.post(
        f"{api_v1}/email/send",
        json={
            "to": ["test@example.com"],
            "subject": "Test",
            "body": "Body",
        },
    )
    assert response.status_code == 401
    assert "detail" in response.json()


def test_email_send_with_invalid_key_returns_401(client, api_v1):
    """With wrong API Key, POST /api/v1/email/send returns 401."""
    response = client.post(
        f"{api_v1}/email/send",
        json={
            "to": ["test@example.com"],
            "subject": "Test",
            "body": "Body",
        },
        headers={"X-API-Key": "wrong-key"},
    )
    assert response.status_code == 401


def test_email_send_with_valid_key_accepts_request(client, api_v1, auth_headers):
    """With valid API Key, POST /api/v1/email/send is accepted (may 500/200 depending on SMTP)."""
    response = client.post(
        f"{api_v1}/email/send",
        json={
            "to": ["test@example.com"],
            "subject": "Test",
            "body": "Body",
        },
        headers=auth_headers,
    )
    # 200 if sent, 500 if SMTP fails (e.g. in CI) - but must not be 401
    assert response.status_code != 401


def test_whatsapp_send_requires_auth(client, api_v1):
    """Without API Key, POST /api/v1/whatsapp/send-whatsapp returns 401."""
    response = client.post(
        f"{api_v1}/whatsapp/send-whatsapp",
        json={"telefono": "573001234567", "mensaje": "Test"},
    )
    assert response.status_code == 401


def test_whatsapp_send_with_valid_key_accepted(client, api_v1, auth_headers):
    """With valid API Key, POST to WhatsApp is accepted (may fail later on provider)."""
    response = client.post(
        f"{api_v1}/whatsapp/send-whatsapp",
        json={"telefono": "573001234567", "mensaje": "Test"},
        headers=auth_headers,
    )
    assert response.status_code != 401


def test_bearer_auth_works(client, api_v1, auth_headers):
    """Authorization: Bearer <api_key> is accepted like X-API-Key."""
    api_key = auth_headers["X-API-Key"]
    response = client.post(
        f"{api_v1}/email/send",
        json={"to": ["test@example.com"], "subject": "Test", "body": "Body"},
        headers={"Authorization": f"Bearer {api_key}"},
    )
    assert response.status_code != 401
