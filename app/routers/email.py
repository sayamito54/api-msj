from fastapi import APIRouter, HTTPException, Depends
from typing import List
import logging

from app.schemas.email_schema import EmailRequest, EmailResponse, EmailStatus
from app.services.email_service import email_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/email", tags=["email"])


@router.post("/send", response_model=EmailResponse)
async def send_email(email_request: EmailRequest):
    """
    Send a single email.
    
    Args:
        email_request: Email request with recipient, subject, and body
        
    Returns:
        EmailResponse with success status and details
    """
    try:
        response = await email_service.send_email(email_request)
        
        if not response.success:
            raise HTTPException(
                status_code=500,
                detail=response.error_details or "Failed to send email"
            )
        
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in send_email endpoint: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Internal server error"
        )


@router.post("/send-bulk", response_model=List[EmailResponse])
async def send_bulk_emails(email_requests: List[EmailRequest]):
    """
    Send multiple emails concurrently.
    
    Args:
        email_requests: List of email requests
        
    Returns:
        List of EmailResponse with success status for each email
    """
    try:
        if not email_requests:
            raise HTTPException(
                status_code=400,
                detail="At least one email request is required"
            )
        
        if len(email_requests) > 100:  # Limit bulk sending
            raise HTTPException(
                status_code=400,
                detail="Maximum 100 emails allowed per bulk request"
            )
        
        responses = await email_service.send_bulk_emails(email_requests)
        return responses
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in send_bulk_emails endpoint: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Internal server error"
        )


@router.get("/health")
async def email_health_check():
    """
    Health check endpoint for email service.
    
    Returns:
        Health status of the email service
    """
    try:
        # Basic health check - could be extended to test SMTP connection
        return {
            "status": "healthy",
            "service": "email",
            "message": "Email service is operational"
        }
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        raise HTTPException(
            status_code=503,
            detail="Email service is not healthy"
        )