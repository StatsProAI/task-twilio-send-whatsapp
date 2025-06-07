from datetime import datetime
from src.config.settings import LOG_FORMAT

def log_message(message, level="INFO"):
    """Função para padronizar o formato dos logs"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(LOG_FORMAT.format(
        timestamp=timestamp,
        level=level,
        message=message
    )) 