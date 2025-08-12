from pydantic import BaseModel, Field
from typing import Optional


class WhatsAppRequest(BaseModel):
    """Schema for WhatsApp sending request using the notificar_oferta template."""
    telefono: str = Field(..., description="Recipient phone number")
    mensaje: str = Field(..., description="Message content to be sent in the template")


class WhatsAppResponse(BaseModel):
    """Schema for WhatsApp sending response."""
    success: bool
    message: str
    message_id: Optional[str] = None
    error_details: Optional[str] = None


class WhatsAppStatus(BaseModel):
    """Schema for WhatsApp status response."""
    message_id: str
    status: str
    sent_at: Optional[str] = None
    error_message: Optional[str] = None
