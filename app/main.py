import logging
import time

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.openapi.utils import get_openapi

from app.config import settings
from app.routers import email, whatsapp

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Docs only when enabled (disable in production via ENABLE_OPENAPI_DOCS=false)
docs_url = "/docs" if settings.enable_openapi_docs else None
redoc_url = "/redoc" if settings.enable_openapi_docs else None
openapi_url = "/openapi.json" if settings.enable_openapi_docs else None

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Microservicio de mensajería/correo. Autenticación servicio a servicio por API Key (header X-API-Key o Authorization: Bearer). Solo es llamado por la API principal (api_ofertame) u otros backends de confianza.",
    docs_url=docs_url,
    redoc_url=redoc_url,
    openapi_url=openapi_url,
    openapi_tags=[
        {"name": "email", "description": "Envío de correos electrónicos"},
        {"name": "whatsapp", "description": "Envío de mensajes WhatsApp"},
    ],
    contact={"name": "API Ofertame", "url": "", "email": ""},
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    """Add processing time header to responses."""
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler. Returns 500 with standard error shape."""
    logger.error(f"Unhandled exception: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )


@app.get("/")
def root():
    """Root endpoint: welcome message, API prefix and version (no auth required)."""
    return {
        "message": "API-MSJ: microservicio de mensajería. Use la base URL con prefijo /api/v1 y envíe el header de API Key en cada petición.",
        "api_v1": "/api/v1",
        "version": settings.app_version,
        "service": settings.app_name,
        "status": "running",
    }


@app.get("/health")
def health_check():
    """Global health check endpoint (no auth required)."""
    return {
        "status": "healthy",
        "service": settings.app_name,
        "version": settings.app_version
    }


# Include routers under /api/v1
app.include_router(email.router, prefix="/api/v1")
app.include_router(whatsapp.router, prefix="/api/v1")


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
        tags=app.openapi_tags,
    )
    # Document API Key security: X-API-Key or Bearer
    openapi_schema["components"]["securitySchemes"] = {
        "ApiKeyHeader": {
            "type": "apiKey",
            "in": "header",
            "name": "X-API-Key",
            "description": "Clave compartida (API_MSJ_SECRET). Alternativa: Authorization: Bearer <api_key>",
        },
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "API Key",
            "description": "Use el mismo valor que API_MSJ_SECRET",
        },
    }
    openapi_schema["security"] = [{"ApiKeyHeader": []}, {"BearerAuth": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug
    )
