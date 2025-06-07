import os
import json
from google.cloud import bigquery
from dotenv import load_dotenv


def get_bigquery_client():
    """
    Cria e retorna um cliente do BigQuery usando as credenciais do arquivo JSON
    """
    # Carrega variáveis do .env
    load_dotenv()
    
    # Caminho para o arquivo de credenciais
    credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    dataset_id = os.getenv("BIGQUERY_DATASET_ID")

    if not credentials_path or not dataset_id:
        raise ValueError("GOOGLE_APPLICATION_CREDENTIALS ou BIGQUERY_DATASET_ID não encontrados no .env")

    # Cria cliente BigQuery usando o arquivo de credenciais
    client = bigquery.Client.from_service_account_json(credentials_path)
    
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