import os
import json
import time
from datetime import datetime
from google.cloud import bigquery
from dotenv import load_dotenv
from queries import get_users
from twilio_service import send_message_with_template
from src.models.user import User
from src.services.batch_processor import BatchProcessor
from src.services.stats_service import StatsService
from src.utils.logger import log_message
from src.config.settings import TWILIO_CONTENT_SID

# Carrega as variáveis de ambiente no início
load_dotenv()


def log_message(message, level="INFO"):
    """Função para padronizar o formato dos logs"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"[{timestamp}] [{level}] {message}")


def print_summary(summary):
    """Função para imprimir o resumo formatado"""
    log_message("="*50)
    log_message("📊 RESUMO DA EXECUÇÃO")
    log_message("="*50)
    
    # Estatísticas principais
    log_message(f"🕒 Data/Hora: {summary['timestamp']}")
    log_message(f"👥 Total de usuários: {summary['total_users']}")
    log_message(f"✅ Mensagens enviadas: {summary['messages_sent']}")
    log_message(f"❌ Mensagens com erro: {summary['messages_failed']}")
    log_message(f"📈 Taxa de sucesso: {summary['success_rate']}")
    log_message(f"⏱️ Tempo total: {summary['execution_time']}")
    
    # Estatísticas de performance
    if summary['total_users'] > 0:
        avg_time = float(summary['execution_time'].replace('s', '')) / summary['total_users']
        log_message(f"⚡ Tempo médio por usuário: {avg_time:.2f}s")
    
    # Detalhes dos erros
    if summary['errors']:
        log_message("\n⚠️ Erros encontrados:", "WARNING")
        for error in summary['errors']:
            log_message(f"❌ Usuário {error['user_id']}: {error['error']}", "ERROR")
    
    # Barra de progresso visual
    if summary['total_users'] > 0:
        success_rate = summary['messages_sent'] / summary['total_users']
        bar_length = 30
        filled_length = int(bar_length * success_rate)
        bar = '█' * filled_length + '░' * (bar_length - filled_length)
        log_message(f"\nProgresso: [{bar}] {summary['success_rate']}")
    
    log_message("="*50)
    
    # Envia resumo para o Slack
    slack_webhook_url = os.getenv('SLACK_WEBHOOK_URL')
    if slack_webhook_url:
        slack_message = format_slack_summary(summary)
        if send_slack_message(slack_webhook_url, slack_message):
            log_message("✓ Resumo enviado para o Slack", "SUCCESS")
        else:
            log_message("✗ Erro ao enviar resumo para o Slack", "ERROR")


def convert_to_user(row) -> User:
    """Converte uma linha do BigQuery para um objeto User"""
    return User(
        user_id=str(row.user_id),
        first_name=str(row.first_name),
        email=str(row.email),
        phone_number=str(row.phone_number) if row.phone_number else None
    )


def process_user(user: User) -> tuple[bool, str]:
    """Processa um usuário individual"""
    if not user.has_valid_phone():
        return False, f"Usuário {user.first_name} não possui número de telefone válido"

    try:
        send_message_with_template(
            content_sid=TWILIO_CONTENT_SID,
            phone_number=user.phone_number,
            content={
                "name": user.first_name,
                "email": user.email
            }
        )
        return True, None
    except Exception as e:
        return False, str(e)


def main():
    try:
        # Inicializa o serviço de estatísticas
        stats = StatsService()
        stats.start()

        # Busca usuários e converte para objetos User
        users = [convert_to_user(row) for row in get_users()]
        if not users:
            log_message("Nenhum usuário encontrado.")
            return

        stats.total_users = len(users)
        log_message(f"Iniciando processamento de {stats.total_users} usuários")

        # Processa usuários em lotes
        processor = BatchProcessor(users)
        successes, failures, errors = processor.process(
            processor_func=process_user,
            progress_desc="Processando usuários"
        )

        # Atualiza estatísticas
        stats.messages_sent = successes
        stats.messages_failed = failures
        stats.errors = errors

        # Finaliza e gera resumo
        stats.end()

    except Exception as e:
        log_message(f"Erro crítico: {str(e)}", "CRITICAL")


if __name__ == "__main__":
    main() 