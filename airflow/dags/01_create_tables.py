from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from datetime import datetime, timedelta

def run_init_sql():
    # Caminho relativo ao container Airflow, ajuste se necessário
    sql_file_path = '/opt/sql/init.sql'
    
    # Ler o conteúdo do arquivo SQL
    with open(sql_file_path, 'r') as file:
        sql_statements = file.read()
    
    # Usar a conexão Postgres configurada no Airflow UI Connections (conn_id='postgres_default' ou seu conn_id)
    hook = PostgresHook(postgres_conn_id='postgres_default')
    
    # Executar o SQL
    hook.run(sql_statements)

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2025, 9, 1),
    'catchup': False,
}

with DAG(
    dag_id='create_postgres_tables',
    default_args=default_args,
    schedule=None,
    tags=['init', 'postgres'],
) as dag:

    init_tables = PythonOperator(
        task_id='run_init_sql',
        python_callable=run_init_sql,
        execution_timeout=timedelta(minutes=2)
    )

    init_tables
