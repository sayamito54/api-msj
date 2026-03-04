# API-MSJ - Microservicio de Notificaciones

Microservicio desarrollado con **FastAPI** para el envío de notificaciones por diferentes canales (email, WhatsApp, SMS).

## 🚀 Características

- **FastAPI** como framework principal
- **aiosmtplib** para envío asíncrono de correos
- **Pydantic** para validación de datos
- Configuración mediante variables de entorno
- Arquitectura por capas (routers, services, schemas)
- Documentación automática con Swagger/OpenAPI
- Preparado para integración con Celery (opcional)

## 📁 Estructura del Proyecto

```
api-msj/
├── app/
│   ├── __init__.py
│   ├── main.py              # Aplicación principal FastAPI
│   ├── config.py            # Configuración y variables de entorno
│   ├── routers/
│   │   ├── __init__.py
│   │   └── email.py         # Endpoints para email
│   ├── services/
│   │   ├── __init__.py
│   │   └── email_service.py # Lógica de negocio para email
│   └── schemas/
│       ├── __init__.py
│       └── email_schema.py  # Modelos Pydantic
├── .env                     # Variables de entorno (crear desde env.example)
├── env.example              # Ejemplo de configuración
├── requirements.txt         # Dependencias del proyecto
└── README.md               # Este archivo
```

## 🛠️ Instalación

### 1. Clonar y configurar el entorno

```bash
# Crear entorno virtual
python -m venv venv-api-msj

# Activar entorno virtual
# Windows:
venv-api-msj\Scripts\activate
# Linux/Mac:
source venv-api-msj/bin/activate

# Desactivar entorno virtual
deactivate

# Instalar dependencias
pip install -r requirements.txt
```

### 2. Configurar variables de entorno

```bash
# Copiar el archivo de ejemplo
cp env.example .env

# Editar .env con tus credenciales SMTP
```

### 3. Configurar credenciales SMTP

Edita el archivo `.env` con tus credenciales:

```env
# SMTP Configuration
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=tu-email@gmail.com
SMTP_PASS=tu-contraseña-de-aplicación
EMAIL_FROM=tu-email@gmail.com

# Application Configuration
APP_NAME=API-MSJ
APP_VERSION=1.0.0
DEBUG=True
```

**Nota:** Para Gmail, necesitas usar una "Contraseña de aplicación" en lugar de tu contraseña normal.

## 🚀 Ejecución

### Desarrollo

```bash
# Ejecutar con uvicorn
uvicorn app.main:app --reload --host 0.0.0.0 --port 9000

# O ejecutar directamente
python -m app.main
```

### Producción

```bash
# Ejecutar con uvicorn en modo producción
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

## 📚 API Endpoints

### Documentación Automática

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

### Endpoints Principales

#### 1. Enviar Email Individual
```http
POST /email/send
Content-Type: application/json

{
  "to": ["destinatario@ejemplo.com"],
  "subject": "Asunto del correo",
  "body": "Contenido del mensaje",
  "cc": ["copia@ejemplo.com"],
  "bcc": ["copia-oculta@ejemplo.com"],
  "priority": "normal",
  "is_html": false
}
```

#### 2. Enviar Emails en Lote
```http
POST /email/send-bulk
Content-Type: application/json

[
  {
    "to": ["destinatario1@ejemplo.com"],
    "subject": "Email 1",
    "body": "Contenido 1"
  },
  {
    "to": ["destinatario2@ejemplo.com"],
    "subject": "Email 2", 
    "body": "Contenido 2"
  }
]
```

#### 3. Health Check
```http
GET /health
GET /email/health
```

## 🔧 Configuración Avanzada

### Integración con Celery (Opcional)

Para habilitar el procesamiento asíncrono con Celery:

1. Descomenta las dependencias en `requirements.txt`:
```txt
celery==5.3.4
redis==5.0.1
```

2. Configura Redis en `.env`:
```env
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0
```

3. Ejecuta el worker de Celery:
```bash
celery -A app.celery_app worker --loglevel=info
```

## 🧪 Testing

### Ejemplo de uso con curl

```bash
# Enviar email simple
curl -X POST "http://localhost:8000/email/send" \
  -H "Content-Type: application/json" \
  -d '{
    "to": ["test@ejemplo.com"],
    "subject": "Test Email",
    "body": "Este es un email de prueba"
  }'

# Health check
curl http://localhost:8000/health
```

## 🔒 Seguridad

- Configura CORS apropiadamente para producción
- Usa variables de entorno para credenciales sensibles
- Considera usar HTTPS en producción
- Implementa autenticación según necesidades

## 🚀 Próximos Pasos

El microservicio está diseñado para ser extensible. Próximas características:

- **WhatsApp Integration:** Usando APIs como Twilio o WhatsApp Business API
- **SMS Integration:** Integración con proveedores SMS
- **Templates:** Sistema de plantillas para emails
- **Rate Limiting:** Control de límites de envío
- **Monitoring:** Métricas y logs avanzados
- **Queue Management:** Sistema de colas para envíos masivos

## 📝 Licencia

Este proyecto está bajo la licencia MIT.

## 🤝 Contribución

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request 