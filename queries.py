from database import get_bigquery_client, get_dataset_id


def get_users():
    """
    Retorna os usuários ativos com número de telefone da view view_user_and_subs_enriched
    """
    client = get_bigquery_client()
    dataset_id = get_dataset_id()
    
    # query = f"""
    # SELECT * 
    # FROM `{dataset_id}.view_user_and_subs_enriched` 
    # WHERE status = 'ativo' 
    # AND phone_number is not null
    # """

    query = f"""
    SELECT * 
    FROM `{dataset_id}.user` 
    WHERE email = 'venturi@statspro.ai'
    """
    
    query_job = client.query(query)
    results = query_job.result()
    
    return results