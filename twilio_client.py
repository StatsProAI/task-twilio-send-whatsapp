import os
from twilio.rest import Client
from dotenv import load_dotenv


def get_twilio_client():
    """
    Cria e retorna um cliente Twilio usando as credenciais do .env
    """
    # Carrega variáveis do .env
    load_dotenv()
    account_sid = os.getenv("TWILIO_ACCOUNT_SID")
    auth_token = os.getenv("TWILIO_AUTH_TOKEN")

    if not account_sid or not auth_token:
        raise ValueError("Twilio credentials are not set in environment variables")

    # Cria cliente Twilio usando as credenciais do env
    client = Client(account_sid, auth_token)
    
    return client 