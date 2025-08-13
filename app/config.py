import os
from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Application
    app_name: str = "API-MSJ"
    app_version: str = "1.0.0"
    debug: bool = True
    
    # SMTP Configuration
    smtp_host: str
    smtp_port: int = 587
    smtp_user: str
    smtp_pass: str
    email_from: str
    smtp_validate_certs: bool = True
    
    # WhatsApp Configuration
    whatsapp_token: str
    whatsapp_url: str
    
    # Optional Celery Configuration
    celery_broker_url: Optional[str] = None
    celery_result_backend: Optional[str] = None
    
    class Config:
        env_file = ".env"
        case_sensitive = False
        extra = "ignore"  # Ignore extra environment variables


# Global settings instance
settings = Settings() 