"""Reusable error response schemas for OpenAPI and consistent API responses."""
from pydantic import BaseModel, Field


class ErrorDetail(BaseModel):
    """Standard error response body."""
    detail: str = Field(..., description="Human-readable error message")


# Use in responses= for OpenAPI: 400, 401, 404, 422, 500
__all__ = ["ErrorDetail"]
