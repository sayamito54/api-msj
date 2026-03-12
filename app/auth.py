"""
Service-to-service authentication via API Key.
No user login; the caller (e.g. api_ofertame) sends the shared secret in every request.
"""
from fastapi import Header, HTTPException, status

from app.config import settings


def verify_api_key(
    x_api_key: str | None = Header(None, alias="X-API-Key", description="API Key for service-to-service auth"),
    authorization: str | None = Header(None, description="Bearer token: Authorization: Bearer <api_key>"),
) -> None:
    """
    Verify API Key from X-API-Key header or Authorization: Bearer <api_key>.
    Raises 401 if missing or not matching API_MSJ_SECRET.
    """
    secret = (settings.api_msj_secret or "").strip()
    if not secret:
        raise HTTPException(
            status_code=status.HTTP_501_NOT_IMPLEMENTED,
            detail="API Key authentication is not configured (API_MSJ_SECRET is empty)",
        )

    provided: str | None = None
    if x_api_key is not None and x_api_key.strip():
        provided = x_api_key.strip()
    elif authorization and authorization.strip().lower().startswith("bearer "):
        provided = authorization.strip()[7:].strip()

    if not provided or provided != secret:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API Key. Use X-API-Key or Authorization: Bearer <api_key>.",
        )
