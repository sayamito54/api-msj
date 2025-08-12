from fastapi import APIRouter, HTTPException
import urllib.request
import urllib.parse
import json
import logging
import os
from app.schemas.whatsapp_schema import WhatsAppRequest, WhatsAppResponse
from app.config import settings

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/whatsapp", tags=["whatsapp"])

@router.post("/send-whatsapp", response_model=WhatsAppResponse)
async def send_whatsapp(request: WhatsAppRequest):
    try:
        # Use v22.0 as per the working documentation
        url = f"https://graph.facebook.com/v22.0/{settings.whatsapp_url}/messages"
        
        # Prepare headers
        headers = {
            "Authorization": f"Bearer {settings.whatsapp_token}",
            "Content-Type": "application/json"
        }
        
        # Build payload with the notificar_oferta template
        payload = {
            "messaging_product": "whatsapp",
            "to": request.telefono,
            "type": "template",
            "template": {
                "name": "notificar_oferta",
                "language": { "code": "es_CO" },
                "components": [
                    {
                        "type": "header",
                        "parameters": [
                            {
                                "type": "image",
                                "image": {
                                    "link": "https://v0-ofertame-app.vercel.app/logo.png"
                                }
                            }
                        ]
                    },
                    {
                        "type": "body",
                        "parameters": [
                            {
                                "type": "text",
                                "text": request.mensaje
                            }
                        ]
                    }
                ]
            }
        }
        
        logger.info(f"Sending WhatsApp message to {request.telefono}")
        logger.info(f"Message: {request.mensaje}")
        logger.info(f"Payload: {json.dumps(payload, indent=2)}")
        
        # Convert payload to JSON string
        data = json.dumps(payload).encode('utf-8')
        
        # Create request
        req = urllib.request.Request(url, data=data, headers=headers, method='POST')
        
        # Send request
        with urllib.request.urlopen(req) as response:
            response_data = json.loads(response.read().decode('utf-8'))
            
            logger.info(f"WhatsApp API response: {json.dumps(response_data, indent=2)}")
            
            if response.status == 200:
                return WhatsAppResponse(
                    success=True,
                    message="WhatsApp message sent successfully",
                    message_id=response_data.get("messages", [{}])[0].get("id")
                )
            else:
                logger.error(f"WhatsApp API error: {response.status} - {response_data}")
                return WhatsAppResponse(
                    success=False,
                    message="Failed to send WhatsApp message",
                    error_details=str(response_data)
                )
            
    except urllib.error.HTTPError as e:
        error_body = e.read().decode('utf-8') if hasattr(e, 'read') else str(e)
        logger.error(f"WhatsApp API HTTP error: {e.code} - {error_body}")
        return WhatsAppResponse(
            success=False,
            message="WhatsApp API error",
            error_details=f"HTTP {e.code}: {error_body}"
        )
    except Exception as e:
        logger.error(f"Error sending WhatsApp message: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/health")
async def whatsapp_health_check():
    """
    Health check endpoint for WhatsApp service.
    """
    try:
        return {
            "status": "healthy",
            "service": "whatsapp",
            "message": "WhatsApp service is operational",
            "template_info": {
                "template_name": "notificar_oferta",
                "language": "es_CO",
                "api_version": "v22.0"
            }
        }
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        raise HTTPException(
            status_code=503,
            detail="WhatsApp service is not healthy"
        )