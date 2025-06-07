import os
import time
from twilio_client import get_twilio_client
from dotenv import load_dotenv


def send_message_with_template(content_sid, phone_number, content=None):
    """
    Envia uma mensagem via WhatsApp usando um template do Twilio.
    
    Args:
        content_sid (str): ID do conteúdo do template.
        phone_number (str): Número de telefone do destinatário.
        content (dict, optional): Conteúdo adicional para o template.
    """
    start_time = time.time()
    try:
        print(f"📤 Sending WhatsApp message to ({phone_number}) contentSid: {content_sid}")
        
        client = get_twilio_client()
        load_dotenv()
        
        message = client.messages.create(
            from_=f"whatsapp:{os.getenv('TWILIO_WHATSAPP_NUMBER')}",
            to=f"whatsapp:{phone_number}",
            content_sid=content_sid,
            messaging_service_sid=os.getenv("TWILIO_MESSAGE_SERVICE_SID"),
        )
        
        duration = (time.time() - start_time) * 1000  # Convert to milliseconds
        print(f"✅ WhatsApp message sent successfully to ({phone_number}) contentSid: {content_sid} in {duration:.2f}ms")
        
    except Exception as error:
        duration = (time.time() - start_time) * 1000  # Convert to milliseconds
        print(f"❌ Failed to send WhatsApp message to ({phone_number}) contentSid: {content_sid} in {duration:.2f}ms: {str(error)}") 