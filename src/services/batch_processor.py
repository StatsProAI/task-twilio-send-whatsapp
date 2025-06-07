from typing import Any, Callable, List, Tuple
from datetime import datetime
import time


def log_message(message, level="INFO"):
    """Função para padronizar o formato dos logs"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"[{timestamp}] [{level}] {message}")


class BatchProcessor:
    """Serviço para processar itens em lotes"""
    
    def __init__(self, items, batch_size=5, batch_delay=1):
        self.items = items
        self.total_items = len(items)
        self.batch_size = batch_size
        self.batch_delay = batch_delay
        self.total_batches = (len(items) + batch_size - 1) // batch_size

    def process(self, processor_func, progress_desc="Processando"):
        """
        Processa os itens em lotes usando a função fornecida
        
        Args:
            processor_func: Função que processa um item individual
            progress_desc: Descrição para a barra de progresso
            
        Returns:
            tuple: (sucessos, falhas, erros)
        """
        successes = 0
        failures = 0
        errors = []
        start_time = datetime.now()

        log_message(f"Iniciando processamento de {self.total_items} itens em lotes de {self.batch_size}")
        log_message(f"Descrição: {progress_desc}")

        for batch_num in range(self.total_batches):
            start_idx = batch_num * self.batch_size
            end_idx = min(start_idx + self.batch_size, self.total_items)
            current_batch = self.items[start_idx:end_idx]
            
            log_message(f"\nProcessando lote {batch_num + 1}/{self.total_batches}")
            log_message(f"Itens {start_idx + 1} até {end_idx}")

            # Processa os itens do lote atual
            for index, item in enumerate(current_batch, start_idx + 1):
                user_id = getattr(item, 'user_id', 'unknown')
                log_message(f"Processando item {index}/{self.total_items} (ID: {user_id})")
                
                try:
                    success, error = processor_func(item)
                    
                    if success:
                        successes += 1
                        log_message(f"✓ Item {index} processado com sucesso", "SUCCESS")
                    else:
                        failures += 1
                        errors.append({
                            'user_id': user_id,
                            'error': error
                        })
                        log_message(f"✗ Erro ao processar item {index}: {error}", "ERROR")
                except Exception as e:
                    failures += 1
                    errors.append({
                        'user_id': user_id,
                        'error': str(e)
                    })
                    log_message(f"✗ Erro inesperado ao processar item {index}: {str(e)}", "ERROR")

            # Aguarda antes do próximo lote (exceto no último lote)
            if batch_num < self.total_batches - 1:
                log_message(f"Aguardando {self.batch_delay} segundo(s) antes do próximo lote...")
                time.sleep(self.batch_delay)

        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        # Resumo do processamento
        log_message("\n" + "=" * 50)
        log_message("📊 RESUMO DO PROCESSAMENTO")
        log_message("=" * 50)
        log_message(f"Total de itens: {self.total_items}")
        log_message(f"Total de lotes: {self.total_batches}")
        log_message(f"Tamanho do lote: {self.batch_size}")
        log_message(f"Sucessos: {successes}")
        log_message(f"Falhas: {failures}")
        log_message(f"Tempo total: {duration:.2f} segundos")
        log_message(f"Taxa de sucesso: {(successes/self.total_items)*100:.1f}%")
        
        if errors:
            log_message("\n⚠️ Erros encontrados:", "WARNING")
            for error in errors:
                log_message(f"❌ Usuário {error['user_id']}: {error['error']}", "ERROR")
        
        log_message("=" * 50)

        return successes, failures, errors 