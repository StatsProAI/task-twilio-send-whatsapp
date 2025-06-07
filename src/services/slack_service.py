import json
import requests
from datetime import datetime

def send_slack_message(webhook_url: str, message: str) -> bool:
    """
    Envia uma mensagem para o Slack usando webhook
    
    Args:
        webhook_url: URL do webhook do Slack
        message: Mensagem a ser enviada
        
    Returns:
        bool: True se a mensagem foi enviada com sucesso, False caso contrário
    """
    try:
        payload = {
            "text": message
        }
        
        response = requests.post(
            webhook_url,
            data=json.dumps(payload),
            headers={'Content-Type': 'application/json'}
        )
        
        return response.status_code == 200
    except Exception as e:
        print(f"Erro ao enviar mensagem para o Slack: {str(e)}")
        return False

def format_slack_summary(summary: dict) -> str:
    """
    Formata o resumo da execução para o Slack
    
    Args:
        summary: Dicionário com as estatísticas da execução
        
    Returns:
        str: Mensagem formatada para o Slack
    """
    message = f"""
📊 *RESUMO DA EXECUÇÃO*
🕒 Data/Hora: {summary['timestamp']}
👥 Total de usuários: {summary['total_users']}
✅ Mensagens enviadas: {summary['messages_sent']}
❌ Mensagens com erro: {summary['messages_failed']}
📈 Taxa de sucesso: {summary['success_rate']}
⏱️ Tempo total: {summary['execution_time']}
"""

    # Estatísticas de performance
    if summary['total_users'] > 0:
        avg_time = float(summary['execution_time'].replace('s', '')) / summary['total_users']
        message += f"⚡ Tempo médio por usuário: {avg_time:.2f}s\n"

    # Detalhes dos erros
    if summary['errors']:
        message += "\n⚠️ *Erros encontrados:*\n"
        for error in summary['errors']:
            message += f"❌ {error}\n"

    # Barra de progresso visual
    if summary['total_users'] > 0:
        success_rate = summary['messages_sent'] / summary['total_users']
        bar_length = 30
        filled_length = int(bar_length * success_rate)
        bar = '█' * filled_length + '░' * (bar_length - filled_length)
        message += f"\nProgresso: [{bar}] {summary['success_rate']}"

    return message 