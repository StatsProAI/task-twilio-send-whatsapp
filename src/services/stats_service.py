from datetime import datetime
from src.utils.logger import log_message
from src.services.slack_service import send_slack_message, format_slack_summary

class StatsService:
    """Serviço para gerenciar estatísticas de execução"""
    
    def __init__(self):
        self.start_time = None
        self.total_users = 0
        self.messages_sent = 0
        self.messages_failed = 0
        self.errors = []

    def start(self):
        """Inicia o registro de estatísticas"""
        self.start_time = datetime.now()
        self._send_start_message()

    def end(self):
        """Finaliza o registro de estatísticas e gera o resumo"""
        if not self.start_time:
            return

        execution_time = (datetime.now() - self.start_time).total_seconds()
        
        summary = {
            "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "total_users": self.total_users,
            "messages_sent": self.messages_sent,
            "messages_failed": self.messages_failed,
            "success_rate": f"{(self.messages_sent/self.total_users)*100:.2f}%" if self.total_users > 0 else "0%",
            "execution_time": f"{execution_time:.2f}s",
            "errors": self.errors
        }
        
        self._print_summary(summary)
        self._send_slack_summary(summary)

    def _print_summary(self, summary):
        """Imprime o resumo formatado"""
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
                log_message(f"❌ {error}", "ERROR")
        
        # Barra de progresso visual
        if summary['total_users'] > 0:
            success_rate = summary['messages_sent'] / summary['total_users']
            bar_length = 30
            filled_length = int(bar_length * success_rate)
            bar = '█' * filled_length + '░' * (bar_length - filled_length)
            log_message(f"\nProgresso: [{bar}] {summary['success_rate']}")
        
        log_message("="*50)

    def _send_start_message(self):
        """Envia mensagem inicial para o Slack"""
        from src.config.settings import SLACK_WEBHOOK_URL
        
        if SLACK_WEBHOOK_URL:
            start_message = f"""
🚀 *INÍCIO DO PROCESSAMENTO*
🕒 Data/Hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
⏳ Iniciando envio de mensagens WhatsApp...
"""
            if send_slack_message(SLACK_WEBHOOK_URL, start_message):
                log_message("✓ Mensagem inicial enviada para o Slack", "SUCCESS")
            else:
                log_message("✗ Erro ao enviar mensagem inicial para o Slack", "ERROR")

    def _send_slack_summary(self, summary):
        """Envia resumo para o Slack"""
        from src.config.settings import SLACK_WEBHOOK_URL
        
        if SLACK_WEBHOOK_URL:
            slack_message = format_slack_summary(summary)
            if send_slack_message(SLACK_WEBHOOK_URL, slack_message):
                log_message("✓ Resumo enviado para o Slack", "SUCCESS")
            else:
                log_message("✗ Erro ao enviar resumo para o Slack", "ERROR") 