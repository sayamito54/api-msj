# API-MSJ - Microservicio de Notificaciones

Microservicio desarrollado con **FastAPI** para el envío de notificaciones por diferentes canales (email, WhatsApp, SMS). Pensado para ser consumido por la API principal (api_ofertame) u otros backends de confianza; **no hay login de usuarios**: la autenticación es **servicio a servicio por API Key**.

## 🚀 Características

- **FastAPI** como framework principal
- **Autenticación por API Key:** header `X-API-Key` o `Authorization: Bearer <api_key>`
- **Versionado de API:** todos los endpoints bajo `/api/v1`
- **aiosmtplib** para envío asíncrono de correos
- **Pydantic** para validación de datos
- Configuración mediante variables de entorno (pydantic-settings)
- Arquitectura por capas (routers, services, schemas, auth)
- Documentación OpenAPI (Swagger/ReDoc) activable/desactivable en producción
- Preparado para integración con Celery (opcional)

## 📁 Estructura del Proyecto

```
api-msj/
├── app/
│   ├── __init__.py
│   ├── main.py              # Aplicación principal FastAPI
│   ├── config.py            # Configuración y variables de entorno
│   ├── auth.py              # Verificación API Key (servicio a servicio)
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── email.py         # Endpoints para email
│   │   └── whatsapp.py      # Endpoints para WhatsApp
│   ├── services/
│   │   ├── __init__.py
│   │   └── email_service.py # Lógica de negocio para email
│   └── schemas/
│       ├── __init__.py
│       ├── email_schema.py
│       ├── whatsapp_schema.py
│       └── error_schemas.py # Esquemas de error reutilizables
├── tests/
│   ├── conftest.py          # Fixtures (client, auth_headers, api_v1)
│   ├── test_main.py
│   └── test_config.py
├── docs/
│   └── postman/             # Colección Postman de ejemplo
├── .env                     # Variables de entorno (crear desde env.example)
├── env.example              # Ejemplo de configuración
├── requirements.txt         # Dependencias del proyecto
└── README.md                # Este archivo
```

## 🔐 Autenticación (servicio a servicio)

No hay flujo de login. Quien llama (por ejemplo **api_ofertame**) debe:

1. **Usar la base URL que incluya el prefijo:** `/api/v1`  
   Ejemplo: `https://api-msj.ejemplo.com/api/v1/email/send`

2. **Enviar en cada petición** a endpoints protegidos uno de estos headers:
   - **`X-API-Key: <valor de API_MSJ_SECRET>`**
   - **`Authorization: Bearer <api_key>`** (mismo valor que `API_MSJ_SECRET`)

El valor se compara con la variable de entorno `API_MSJ_SECRET` configurada en api-msj. Si falta el header o no coincide, la API responde **401 Unauthorized**.

En **api_ofertame** (o el cliente): configura en `.env` la misma clave, por ejemplo `API_MSJ_SECRET=tu-clave-compartida`, y envíala en cada petición a api-msj.

## 🛠️ Instalación

### 1. Clonar y configurar el entorno

```bash
python -m venv venv-api-msj
# Windows:
venv-api-msj\Scripts\activate
# Linux/Mac:
source venv-api-msj/bin/activate
pip install -r requirements.txt
```

### 2. Configurar variables de entorno

```bash
cp env.example .env
# Editar .env con credenciales y API_MSJ_SECRET
```

Variables relevantes en `.env`:

```env
# Obligatorio para endpoints protegidos (enviar este valor en X-API-Key o Bearer)
API_MSJ_SECRET=your-shared-secret-here

# Desactivar docs en producción
ENABLE_OPENAPI_DOCS=True

# SMTP
SMTP_HOST=smtp-relay.brevo.com
SMTP_PORT=587
SMTP_USER=...
SMTP_PASS=...
EMAIL_FROM=...

# WhatsApp
WHATSAPP_TOKEN=...
WHATSAPP_URL=...
ACTIVAR_WHATSAPP=True

# App
APP_NAME=API-MSJ
APP_VERSION=1.0.0
DEBUG=True
```

## 🚀 Ejecución

```bash
# Desarrollo
uvicorn app.main:app --reload --host 0.0.0.0 --port 9000

# Producción
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

## 📚 API Endpoints

### Base URL y versión

- **GET /** — Mensaje de bienvenida, prefijo de la API y versión (sin auth):
  - `api_v1`: `"/api/v1"`
  - `version`: valor de `APP_VERSION`
- **GET /health** — Health check global (sin auth)

Todos los endpoints de operaciones están bajo **`/api/v1`** y **requieren** el header de API Key (salvo los health de cada recurso).

### Documentación OpenAPI

Cuando `ENABLE_OPENAPI_DOCS=True` (por defecto):

- **Swagger UI:** `http://localhost:8000/docs`
- **ReDoc:** `http://localhost:8000/redoc`
- **openapi.json:** `http://localhost:8000/openapi.json`

En producción, pon `ENABLE_OPENAPI_DOCS=false` para desactivar `/docs`, `/redoc` y opcionalmente `/openapi.json`.

### Endpoints principales (todos bajo `/api/v1`)

#### 1. Enviar email individual

```http
POST /api/v1/email/send
Content-Type: application/json
X-API-Key: <valor de API_MSJ_SECRET>

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

#### 2. Enviar emails en lote

```http
POST /api/v1/email/send-bulk
Content-Type: application/json
X-API-Key: <valor de API_MSJ_SECRET>

[
  { "to": ["dest1@ejemplo.com"], "subject": "Email 1", "body": "Contenido 1" },
  { "to": ["dest2@ejemplo.com"], "subject": "Email 2", "body": "Contenido 2" }
]
```

#### 3. Enviar WhatsApp

```http
POST /api/v1/whatsapp/send-whatsapp
Content-Type: application/json
X-API-Key: <valor de API_MSJ_SECRET>

{
  "telefono": "573001234567",
  "mensaje": "Texto del mensaje"
}
```

#### 4. Health por recurso (sin auth)

```http
GET /health
GET /api/v1/email/health
GET /api/v1/whatsapp/health
```

## 🧪 Ejemplos de uso

### curl con API Key

```bash
# Header X-API-Key
curl -X POST "http://localhost:8000/api/v1/email/send" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-shared-secret-here" \
  -d '{
    "to": ["test@ejemplo.com"],
    "subject": "Test Email",
    "body": "Este es un email de prueba"
  }'

# Alternativa: Authorization Bearer
curl -X POST "http://localhost:8000/api/v1/email/send" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your-shared-secret-here" \
  -d '{"to": ["test@ejemplo.com"], "subject": "Test", "body": "Cuerpo"}'

# Health (sin header)
curl http://localhost:8000/health
curl http://localhost:8000/
```

### Postman

- Importa la colección en `docs/postman/api-msj.postman_collection.json`.
- Configura la variable de colección `base_url` (ej. `http://localhost:8000`) y `api_key` con el valor de `API_MSJ_SECRET`.
- Todas las peticiones a `/api/v1/*` usan la URL base y el header de API Key.

## 🧪 Tests

```bash
pytest tests/ -v
```

Los tests usan el prefijo `/api/v1` y un header de API Key inyectado por fixture (`conftest.py`). Hay pruebas que verifican 401 cuando falta o es incorrecta la clave.

## 🔒 Seguridad

- Autenticación servicio a servicio por API Key (`X-API-Key` o `Authorization: Bearer`).
- Configuración sensible (claves, URLs de proveedores) solo desde variables de entorno o `.env`; nada hardcodeado.
- En producción: `ENABLE_OPENAPI_DOCS=false` para no exponer documentación.
- CORS y HTTPS según tu entorno de producción.

## 📋 Resumen para quien integre (api_ofertame)

- **Base URL:** incluir el prefijo `/api/v1` (ej. `https://api-msj.ejemplo.com/api/v1`).
- **En cada petición** a api-msj enviar el header de API Key (`X-API-Key: <valor>` o `Authorization: Bearer <valor>`) con el secreto compartido configurado en `.env` (`API_MSJ_SECRET`).
- No hay flujo de login en api-msj; la autenticación es servicio a servicio por clave.

## 📝 Licencia

Este proyecto está bajo la licencia MIT.
