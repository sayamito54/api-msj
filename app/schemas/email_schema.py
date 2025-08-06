from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from enum import Enum


class EmailPriority(str, Enum):
    """Email priority levels."""
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"


class EmailRequest(BaseModel):
    """Schema for email sending request."""
    to: List[EmailStr] = Field(..., description="List of recipient email addresses")
    subject: str = Field(..., min_length=1, max_length=200, description="Email subject")
    body: str = Field(..., min_length=1, description="Email body content")
    cc: Optional[List[EmailStr]] = Field(default=None, description="CC recipients")
    bcc: Optional[List[EmailStr]] = Field(default=None, description="BCC recipients")
    priority: EmailPriority = Field(default=EmailPriority.NORMAL, description="Email priority")
    is_html: bool = Field(default=False, description="Whether the body is HTML content")


class EmailResponse(BaseModel):
    """Schema for email sending response."""
    success: bool
    message: str
    email_id: Optional[str] = None
    error_details: Optional[str] = None


class EmailStatus(BaseModel):
    """Schema for email status response."""
    email_id: str
    status: str
    sent_at: Optional[str] = None
    error_message: Optional[str] = None 