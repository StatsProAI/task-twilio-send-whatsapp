import os
from dotenv import load_dotenv

# Carrega as variáveis de ambiente
load_dotenv()

# Configurações do Twilio
TWILIO_CONTENT_SID = "HX822cc2981c1df481023dc2cd99b50704"

# Configurações do Slack
SLACK_WEBHOOK_URL = os.getenv('SLACK_WEBHOOK_URL')

# Configurações de processamento
BATCH_SIZE = 5
BATCH_DELAY = 1  # segundos

# Configurações de logging
LOG_FORMAT = "[{timestamp}] [{level}] {message}" 