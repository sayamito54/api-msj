#!/usr/bin/env python3
"""
Create .env file with correct encoding
"""

def create_env_file():
    """Create .env file with UTF-8 encoding."""
    env_content = """# Brevo SMTP Configuration (Working Configuration)
SMTP_HOST=smtp-relay.brevo.com
SMTP_PORT=587
SMTP_USER=93ee75001@smtp-brevo.com
SMTP_PASS=tu-api-key-brevo
EMAIL_FROM=notebook.sayamito@gmail.com
SMTP_VALIDATE_CERTS=false

# Application Configuration
APP_NAME=API-MSJ
APP_VERSION=1.0.0
DEBUG=True
"""
    
    try:
        with open('.env', 'w', encoding='utf-8') as f:
            f.write(env_content)
        print("✅ Archivo .env creado exitosamente con codificación UTF-8")
        print("📝 Recuerda reemplazar 'tu-api-key-brevo' con tu API key real")
        return True
    except Exception as e:
        print(f"❌ Error creando .env: {e}")
        return False

if __name__ == "__main__":
    create_env_file() 