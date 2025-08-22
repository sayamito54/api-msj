# Servicio de WhatsApp - API-MSJ

## Descripción

El servicio de WhatsApp ha sido actualizado para utilizar la plantilla `notificar_oferta` de WhatsApp Business API. Este servicio permite enviar notificaciones personalizadas a través de WhatsApp usando una plantilla pre-aprobada.

## Características

- ✅ **Plantilla pre-aprobada**: Utiliza la plantilla `notificar_oferta` aprobada por WhatsApp
- ✅ **Imagen de header**: Incluye automáticamente el logo de la aplicación
- ✅ **Mensaje personalizable**: El contenido del mensaje se puede personalizar
- ✅ **Idioma configurado**: Configurado para español colombiano (es_CO)
- ✅ **API v22.0**: Utiliza la versión más reciente de la API de WhatsApp

## Endpoint

### POST `/whatsapp/send-whatsapp`

Envía una notificación de WhatsApp usando la plantilla `notificar_oferta`.

#### Request Body

```json
{
  "telefono": "573001234567",
  "mensaje": "¡Nueva oferta disponible! Descuento del 20% en todos los productos."
}
```

#### Parámetros

- `telefono` (string, requerido): Número de teléfono del destinatario en formato internacional (ej: 573001234567)
- `mensaje` (string, requerido): Contenido del mensaje personalizado

#### Response

```json
{
  "success": true,
  "message": "WhatsApp message sent successfully",
  "message_id": "wamid.1234567890"
}
```

## Estructura de la Plantilla

El servicio transforma automáticamente tu solicitud a la siguiente estructura de WhatsApp API:

```json
{
  "messaging_product": "whatsapp",
  "to": "numero_api-msj",
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
            "text": "Mensaje que llega del servicio de la api-msj"
          }
        ]
      }
    ]
  }
}
```

## Ejemplos de Uso

### 1. Notificación de Oferta

```bash
curl -X POST "http://localhost:8000/whatsapp/send-whatsapp" \
  -H "Content-Type: application/json" \
  -d '{
    "telefono": "573001234567",
    "mensaje": "¡Nueva oferta disponible! Descuento del 20% en todos los productos."
  }'
```

### 2. Notificación de Promoción

```bash
curl -X POST "http://localhost:8000/whatsapp/send-whatsapp" \
  -H "Content-Type: application/json" \
  -d '{
    "telefono": "573001234567",
    "mensaje": "¡Promoción especial! Envío gratis en compras superiores a $100.000"
  }'
```

### 3. Notificación Personalizada

```bash
curl -X POST "http://localhost:8000/whatsapp/send-whatsapp" \
  -H "Content-Type: application/json" \
  -d '{
    "telefono": "573001234567",
    "mensaje": "Hola! Tenemos novedades que te pueden interesar. ¡Contáctanos!"
  }'
```

## Archivo de Ejemplo

Se incluye un archivo `example_whatsapp_usage.py` que demuestra cómo usar el servicio:

```bash
python example_whatsapp_usage.py
```

## Endpoints Adicionales

### GET `/whatsapp/health`

Verifica el estado del servicio de WhatsApp.

```json
{
  "status": "healthy",
  "service": "whatsapp",
  "message": "WhatsApp service is operational",
  "template_info": {
    "template_name": "notificar_oferta",
    "language": "es_CO",
    "api_version": "v22.0"
  }
}
```

## Configuración Requerida

Asegúrate de tener configuradas las siguientes variables de entorno en tu archivo `.env`:

```env
WHATSAPP_TOKEN=tu_token_de_whatsapp
WHATSAPP_URL=tu_phone_number_id
```

## Ventajas de la Plantilla

1. **Cumplimiento de Políticas**: Las plantillas están pre-aprobadas por WhatsApp
2. **Sin Restricciones de 24h**: Puedes enviar mensajes en cualquier momento
3. **Imagen Automática**: El logo se incluye automáticamente en el header
4. **Personalización**: El mensaje del body se puede personalizar completamente
5. **Idioma Local**: Configurado para español colombiano

## Notas Importantes

- El número de teléfono debe incluir el código de país (ej: 57 para Colombia)
- El mensaje se inserta en el componente `body` de la plantilla
- La imagen del logo se obtiene desde `https://v0-ofertame-app.vercel.app/logo.png`
- El servicio utiliza la API v22.0 de WhatsApp Graph API

## Solución de Problemas

### Error de Autenticación
- Verifica que `WHATSAPP_TOKEN` esté configurado correctamente
- Asegúrate de que el token tenga permisos para enviar mensajes

### Error de Plantilla
- Verifica que la plantilla `notificar_oferta` esté aprobada en tu cuenta de WhatsApp Business
- Confirma que `WHATSAPP_URL` apunte al `phone_number_id` correcto

### Error de Número
- Asegúrate de que el número de teléfono esté en formato internacional
- Verifica que el número esté registrado en WhatsApp

## Documentación Adicional

- [WhatsApp Business API Documentation](https://developers.facebook.com/docs/whatsapp)
- [Template Messages](https://developers.facebook.com/docs/whatsapp/message-templates)
- [API Reference](https://developers.facebook.com/docs/whatsapp/cloud-api/reference)




