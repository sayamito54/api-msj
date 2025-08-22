import pytest
from unittest.mock import patch
from app.config import Settings


def test_settings_defaults():
    """Test that settings have correct default values."""
    with patch.dict('os.environ', {}, clear=True):
        settings = Settings()
        assert settings.app_name == "API-MSJ"
        assert settings.app_version == "1.0.0"
        assert settings.debug is True
        assert settings.smtp_port == 587
        assert settings.smtp_validate_certs is True


def test_settings_from_env():
    """Test that settings can be loaded from environment variables."""
    env_vars = {
        "SMTP_HOST": "smtp.gmail.com",
        "SMTP_PORT": "587",
        "SMTP_USER": "test@example.com",
        "SMTP_PASS": "test_password",
        "EMAIL_FROM": "test@example.com",
        "WHATSAPP_TOKEN": "test_token",
        "WHATSAPP_URL": "https://api.whatsapp.com",
        "DEBUG": "false"
    }
    
    with patch.dict('os.environ', env_vars, clear=True):
        settings = Settings()
        assert settings.smtp_host == "smtp.gmail.com"
        assert settings.smtp_port == 587
        assert settings.smtp_user == "test@example.com"
        assert settings.smtp_pass == "test_password"
        assert settings.email_from == "test@example.com"
        assert settings.whatsapp_token == "test_token"
        assert settings.whatsapp_url == "https://api.whatsapp.com"
        assert settings.debug is False


def test_settings_case_insensitive():
    """Test that settings are case insensitive."""
    env_vars = {
        "smtp_host": "smtp.gmail.com",
        "SMTP_USER": "test@example.com"
    }
    
    with patch.dict('os.environ', env_vars, clear=True):
        settings = Settings()
        assert settings.smtp_host == "smtp.gmail.com"
        assert settings.smtp_user == "test@example.com"


def test_optional_celery_settings():
    """Test that optional Celery settings can be None."""
    with patch.dict('os.environ', {}, clear=True):
        settings = Settings()
        assert settings.celery_broker_url is None
        assert settings.celery_result_backend is None


def test_celery_settings_from_env():
    """Test that Celery settings can be loaded from environment."""
    env_vars = {
        "CELERY_BROKER_URL": "redis://localhost:6379/0",
        "CELERY_RESULT_BACKEND": "redis://localhost:6379/0"
    }
    
    with patch.dict('os.environ', env_vars, clear=True):
        settings = Settings()
        assert settings.celery_broker_url == "redis://localhost:6379/0"
        assert settings.celery_result_backend == "redis://localhost:6379/0"
