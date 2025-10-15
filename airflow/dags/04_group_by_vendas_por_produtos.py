from airflow import DAG
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.operators.python import PythonOperator
from datetime import datetime

def executar_sql_upsert():
    caminho_sql = '/opt/sql/group_by.sql'  
    with open(caminho_sql, 'r', encoding='utf-8') as arquivo_sql:
        sql = arquivo_sql.read()
    
    hook = PostgresHook(postgres_conn_id='postgres_default')
    hook.run(sql)

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2025, 9, 12),
    'retries': 1
}

with DAG(
    dag_id='calcula_vendas_por_produtos',
    default_args=default_args,
    schedule='@daily',
    catchup=False,
    max_active_runs=1
) as dag:
    executar_sql_task = PythonOperator(
        task_id='executar_sql_upsert',
        python_callable=executar_sql_upsert
    )
