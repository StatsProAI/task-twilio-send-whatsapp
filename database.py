import os
import json
from google.cloud import bigquery
from dotenv import load_dotenv


def get_bigquery_client():
    """
    Cria e retorna um cliente do BigQuery usando as credenciais do .env
    """
    # Carrega variáveis do .env
    load_dotenv()
    credentials_json = os.getenv("GOOGLE_CREDENTIALS")
    dataset_id = os.getenv("BIGQUERY_DATASET_ID")

    if not credentials_json or not dataset_id:
        raise ValueError("BIGQUERY_DATASET_ID ou GOOGLE_CREDENTIALS não encontrados no .env")

    # Cria cliente BigQuery usando as credenciais do env
    credentials_dict = json.loads(credentials_json)
    client = bigquery.Client.from_service_account_info(credentials_dict)
    
    return client


def get_dataset_id():
    """
    Retorna o ID do dataset do BigQuery
    """
    load_dotenv()
    dataset_id = os.getenv("BIGQUERY_DATASET_ID")
    if not dataset_id:
        raise ValueError("BIGQUERY_DATASET_ID não encontrado no .env")
    return dataset_id 