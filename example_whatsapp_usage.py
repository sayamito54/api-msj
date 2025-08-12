#!/usr/bin/env python3
"""
Ejemplo de uso del endpoint /send-whatsapp

Este archivo muestra cómo usar el servicio de WhatsApp actualizado
que utiliza la plantilla 'notificar_oferta'.
"""

import requests
import json

# Configuración del servicio
API_BASE_URL = "http://localhost:8000"
WHATSAPP_ENDPOINT = f"{API_BASE_URL}/whatsapp/send-whatsapp"

def send_whatsapp_notification(telefono: str, mensaje: str):
    """
    Envía una notificación de WhatsApp usando la plantilla 'notificar_oferta'.
    
    Args:
        telefono (str): Número de teléfono del destinatario (formato: 573001234567)
        mensaje (str): Mensaje personalizado a enviar
    
    Returns:
        dict: Respuesta del API
    """
    
    # Datos de la petición
    payload = {
        "telefono": telefono,
        "mensaje": mensaje
    }
    
    try:
        # Realizar la petición POST
        response = requests.post(
            WHATSAPP_ENDPOINT,
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        
        # Procesar la respuesta
        if response.status_code == 200:
            result = response.json()
            print("✅ WhatsApp enviado exitosamente!")
            print(f"   Message ID: {result.get('message_id')}")
            print(f"   Mensaje: {result.get('message')}")
            return result
        else:
            print(f"❌ Error al enviar WhatsApp: {response.status_code}")
            print(f"   Detalles: {response.text}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Error de conexión: {e}")
        return None

def test_whatsapp_service():
    """Función de prueba para el servicio de WhatsApp."""
    
    print("🚀 Probando el servicio de WhatsApp...")
    print("=" * 50)
    
    # Ejemplo 1: Notificación de oferta
    print("\n📱 Ejemplo 1: Notificación de oferta")
    print("-" * 30)
    result1 = send_whatsapp_notification(
        telefono="573001234567",  # Reemplaza con un número real
        mensaje="¡Nueva oferta disponible! Descuento del 20% en todos los productos."
    )
    
    # Ejemplo 2: Notificación de promoción
    print("\n📱 Ejemplo 2: Notificación de promoción")
    print("-" * 30)
    result2 = send_whatsapp_notification(
        telefono="573001234567",  # Reemplaza con un número real
        mensaje="¡Promoción especial! Envío gratis en compras superiores a $100.000"
    )
    
    # Ejemplo 3: Notificación personalizada
    print("\n📱 Ejemplo 3: Notificación personalizada")
    print("-" * 30)
    result3 = send_whatsapp_notification(
        telefono="573001234567",  # Reemplaza con un número real
        mensaje="Hola! Tenemos novedades que te pueden interesar. ¡Contáctanos!"
    )

def check_service_health():
    """Verifica el estado del servicio."""
    
    try:
        health_url = f"{API_BASE_URL}/whatsapp/health"
        response = requests.get(health_url)
        
        if response.status_code == 200:
            health_data = response.json()
            print("🏥 Estado del servicio WhatsApp:")
            print(f"   Status: {health_data.get('status')}")
            print(f"   Template: {health_data.get('template_info', {}).get('template_name')}")
            print(f"   Idioma: {health_data.get('template_info', {}).get('language')}")
            return True
        else:
            print(f"❌ Servicio no disponible: {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ No se puede conectar al servicio: {e}")
        return False

if __name__ == "__main__":
    print("🔧 Servicio de WhatsApp - API-MSJ")
    print("=" * 50)
    
    # Verificar estado del servicio
    if check_service_health():
        print("\n✅ Servicio disponible. Procediendo con las pruebas...")
        test_whatsapp_service()
    else:
        print("\n❌ Servicio no disponible. Asegúrate de que esté ejecutándose.")
        print("   Comando para iniciar: uvicorn app.main:app --reload")
    
    print("\n" + "=" * 50)
    print("📚 Para más información, visita: /docs")
    print("🔍 Health check: /whatsapp/health")
