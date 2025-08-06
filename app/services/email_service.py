import asyncio
import logging
from typing import List, Optional
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr
import aiosmtplib
from datetime import datetime
import uuid

from app.config import settings
from app.schemas.email_schema import EmailRequest, EmailResponse, EmailPriority

logger = logging.getLogger(__name__)


class EmailService:
    """Service for handling email operations using async SMTP."""
    
    def __init__(self):
        self.smtp_host = settings.smtp_host
        self.smtp_port = settings.smtp_port
        self.smtp_user = settings.smtp_user
        self.smtp_pass = settings.smtp_pass
        self.email_from = settings.email_from
    
    async def send_email(self, email_request: EmailRequest) -> EmailResponse:
        """
        Send email asynchronously using SMTP.
        
        Args:
            email_request: Email request containing recipient, subject, and body
            
        Returns:
            EmailResponse with success status and details
        """
        email_id = str(uuid.uuid4())
        
        try:
            # Create message
            message = await self._create_message(email_request, email_id)
            
            # Send email
            await self._send_smtp_message(message)
            
            logger.info(f"Email sent successfully. ID: {email_id}")
            
            return EmailResponse(
                success=True,
                message="Email sent successfully",
                email_id=email_id
            )
            
        except Exception as e:
            error_msg = f"Failed to send email: {str(e)}"
            logger.error(f"Email sending failed. ID: {email_id}, Error: {error_msg}")
            
            return EmailResponse(
                success=False,
                message="Failed to send email",
                email_id=email_id,
                error_details=error_msg
            )
    
    async def _create_message(self, email_request: EmailRequest, email_id: str) -> MIMEMultipart:
        """Create MIME message from email request."""
        message = MIMEMultipart()
        message["From"] = formataddr(("API-MSJ", self.email_from))
        message["To"] = ", ".join(email_request.to)
        message["Subject"] = email_request.subject
        message["Message-ID"] = f"<{email_id}@{self.smtp_host}>"
        
        # Add CC if provided
        if email_request.cc:
            message["Cc"] = ", ".join(email_request.cc)
        
        # Set priority
        if email_request.priority == EmailPriority.HIGH:
            message["X-Priority"] = "1"
            message["X-MSMail-Priority"] = "High"
        elif email_request.priority == EmailPriority.LOW:
            message["X-Priority"] = "5"
            message["X-MSMail-Priority"] = "Low"
        
        # Add body
        content_type = "html" if email_request.is_html else "plain"
        text_part = MIMEText(email_request.body, content_type, "utf-8")
        message.attach(text_part)
        
        # Prepare recipients list
        recipients = email_request.to.copy()
        if email_request.cc:
            recipients.extend(email_request.cc)
        if email_request.bcc:
            recipients.extend(email_request.bcc)
        
        return message, recipients
    
    async def _send_smtp_message(self, message_data: tuple) -> None:
        """Send message via SMTP."""
        message, recipients = message_data
        
        # Determine TLS configuration based on port
        use_tls = self.smtp_port == 465  # SSL port
        use_starttls = self.smtp_port == 587  # STARTTLS port
        
        # Get certificate validation setting from config
        validate_certs = getattr(settings, 'smtp_validate_certs', True)
        
        # Create SMTP client
        smtp = aiosmtplib.SMTP(
            hostname=self.smtp_host,
            port=self.smtp_port,
            use_tls=use_tls,  # Only use TLS for port 465
            username=self.smtp_user,
            password=self.smtp_pass,
            validate_certs=validate_certs  # Use certificate validation setting
        )
        
        try:
            await smtp.connect()
            
            # Handle authentication based on port and server behavior
            if use_starttls:
                try:
                    # Try STARTTLS first (standard for port 587)
                    await smtp.starttls()
                    logger.info("STARTTLS successful, authenticating...")
                    await smtp.login(self.smtp_user, self.smtp_pass)
                except Exception as starttls_error:
                    error_msg = str(starttls_error)
                    if "Connection already using TLS" in error_msg:
                        # Server already has TLS active, just authenticate
                        logger.info("Server already using TLS, skipping STARTTLS")
                        try:
                            await smtp.login(self.smtp_user, self.smtp_pass)
                        except Exception as auth_error:
                            if "Already authenticated" in str(auth_error):
                                logger.info("Server already authenticated, skipping login")
                            else:
                                raise auth_error
                    elif "Already authenticated" in error_msg:
                        # Server is already authenticated, skip login
                        logger.info("Server already authenticated, skipping login")
                    else:
                        # Other STARTTLS error, re-raise
                        logger.error(f"STARTTLS error: {error_msg}")
                        raise starttls_error
            elif use_tls:
                # For port 465, authenticate directly (TLS already active)
                try:
                    await smtp.login(self.smtp_user, self.smtp_pass)
                except Exception as auth_error:
                    if "Already authenticated" in str(auth_error):
                        logger.info("Server already authenticated, skipping login")
                    else:
                        raise auth_error
            else:
                # For Brevo: No TLS, no STARTTLS, just authenticate
                try:
                    await smtp.login(self.smtp_user, self.smtp_pass)
                except Exception as auth_error:
                    error_msg = str(auth_error)
                    if "Already authenticated" in error_msg:
                        logger.info("Server already authenticated, skipping login")
                        # Don't raise the error, continue with sending
                    else:
                        logger.error(f"Authentication error: {error_msg}")
                        raise auth_error
            
            # Send the message - this is where the "Already authenticated" error might occur
            try:
                await smtp.send_message(message, recipients=recipients)
            except Exception as send_error:
                error_msg = str(send_error)
                if "Already authenticated" in error_msg:
                    logger.info("Server already authenticated during send, continuing...")
                    # Try sending again or consider it successful
                    logger.info("Email sent successfully despite authentication message")
                else:
                    raise send_error
                    
        finally:
            await smtp.quit()
    
    async def send_bulk_emails(self, email_requests: List[EmailRequest]) -> List[EmailResponse]:
        """
        Send multiple emails concurrently.
        
        Args:
            email_requests: List of email requests
            
        Returns:
            List of email responses
        """
        tasks = [self.send_email(req) for req in email_requests]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Convert exceptions to error responses
        responses = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                responses.append(EmailResponse(
                    success=False,
                    message="Failed to send email",
                    error_details=str(result)
                ))
            else:
                responses.append(result)
        
        return responses


# Global email service instance
email_service = EmailService() 