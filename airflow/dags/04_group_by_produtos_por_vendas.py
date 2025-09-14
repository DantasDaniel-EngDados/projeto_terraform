from airflow import DAG
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.operators.python import PythonOperator
from datetime import datetime
import csv

def salvar_resultado():
    caminho_sql = '/opt/sql/group_by.sql'  # Caminho absoluto dentro do container
    with open(caminho_sql, 'r', encoding='utf-8') as arquivo_sql:
        sql = arquivo_sql.read()
    
    hook = PostgresHook(postgres_conn_id='postgres_default')
    resultados = hook.get_records(sql)
    colnames = ['nomeproduto', 'quantidade_total', 'valor_total_venda']
    caminho_arquivo = '/tmp/venda_produtos.csv'
    with open(caminho_arquivo, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(colnames)
        writer.writerows(resultados)


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
    salvar_task = PythonOperator(
        task_id='salvar_resultado',
        python_callable=salvar_resultado
    )
