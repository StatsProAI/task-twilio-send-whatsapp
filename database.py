import os
import json
from google.cloud import bigquery
from dotenv import load_dotenv


def get_bigquery_client():
    """
    Cria e retorna um cliente do BigQuery usando as credenciais do arquivo JSON
    ou da string JSON diretamente do ambiente, dependendo do ambiente (dev/prod)
    """
    # Carrega variáveis do .env
    load_dotenv()
    
    # Obtém o ambiente atual
    env = os.getenv("ENV", "dev").lower()
    credentials_json = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    dataset_id = os.getenv("BIGQUERY_DATASET_ID")

    if not credentials_json or not dataset_id:
        raise ValueError("GOOGLE_APPLICATION_CREDENTIALS ou BIGQUERY_DATASET_ID não encontrados no .env")

    try:
        if env == "prod":
            # Em produção, usa a string JSON diretamente do ambiente
            credentials_info = json.loads(credentials_json)
            client = bigquery.Client.from_service_account_info(credentials_info)
        else:
            # Em desenvolvimento, usa o arquivo de credenciais
            client = bigquery.Client.from_service_account_json(credentials_json)
        
        return client
    except Exception as e:
        raise ValueError(
            f"Não foi possível criar o cliente do BigQuery no ambiente {env}. "
            "Verifique se as credenciais estão corretas. "
            f"Erro: {str(e)}"
        )


def get_dataset_id():
    """
    Retorna o ID do dataset do BigQuery
    """
    load_dotenv()
    dataset_id = os.getenv("BIGQUERY_DATASET_ID")
    if not dataset_id:
        raise ValueError("BIGQUERY_DATASET_ID não encontrado no .env")
    return dataset_id 