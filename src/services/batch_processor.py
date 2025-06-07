import time
from typing import List, Callable, Any
from tqdm import tqdm
from src.utils.logger import log_message
from src.config.settings import BATCH_SIZE, BATCH_DELAY

class BatchProcessor:
    """Serviço para processar itens em lotes"""
    
    def __init__(self, items: List[Any], batch_size: int = BATCH_SIZE):
        self.items = items
        self.batch_size = batch_size
        self.total_batches = (len(items) + batch_size - 1) // batch_size

    def process(self, processor_func: Callable[[Any], tuple[bool, str]], 
                progress_desc: str = "Processando itens") -> tuple[int, int, list]:
        """
        Processa os itens em lotes
        
        Args:
            processor_func: Função que processa um item individual
            progress_desc: Descrição para a barra de progresso
            
        Returns:
            tuple: (sucessos, falhas, erros)
        """
        successes = 0
        failures = 0
        errors = []

        with tqdm(total=len(self.items), desc=progress_desc, unit="item") as pbar:
            for i in range(0, len(self.items), self.batch_size):
                batch = self.items[i:i + self.batch_size]
                current_batch = i//self.batch_size + 1
                log_message(f"Lote {current_batch}/{self.total_batches} iniciado")
                
                for item in batch:
                    try:
                        success, error = processor_func(item)
                        if success:
                            successes += 1
                        else:
                            failures += 1
                            errors.append(error)
                    except Exception as e:
                        failures += 1
                        errors.append(str(e))
                    
                    pbar.update(1)
                
                # Aguarda antes do próximo lote
                if i + self.batch_size < len(self.items):
                    log_message(f"Aguardando {BATCH_DELAY} segundo(s) antes do próximo lote...")
                    time.sleep(BATCH_DELAY)

        return successes, failures, errors 