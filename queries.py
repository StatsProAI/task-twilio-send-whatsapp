from database import get_bigquery_client, get_dataset_id


def get_users():
    """
    Retorna os usuários ativos com número de telefone da view view_user_and_subs_enriched
    """
    client = get_bigquery_client()
    dataset_id = get_dataset_id()
    
    query = f"""
    SELECT * 
    FROM `{dataset_id}.view_user_and_subs_enriched` 
    WHERE status = 'ativo' 
    AND phone_number is not null
    """
    
    query_job = client.query(query)
    results = query_job.result()
    
    return results


def get_user_by_id(user_id):
    """
    Retorna um usuário específico pelo ID
    """
    client = get_bigquery_client()
    dataset_id = get_dataset_id()
    
    query = f"""
    SELECT user_id, full_name, email, phone_number
    FROM `{dataset_id}.user`
    WHERE user_id = @user_id
    """
    
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("user_id", "STRING", user_id),
        ]
    )
    
    query_job = client.query(query, job_config=job_config)
    results = query_job.result()
    
    return results 