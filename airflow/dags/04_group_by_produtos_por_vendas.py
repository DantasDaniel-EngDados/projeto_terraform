from airflow import DAG
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.operators.python import PythonOperator
from datetime import datetime
import csv

def salvar_resultado():
    hook = PostgresHook(postgres_conn_id='postgres_default')
    sql = '''
        SELECT 
            v.nomeproduto,
            SUM(v.quantidade) AS quantidade_total,
            SUM(v.quantidade * p.preco) AS valor_total_venda
        FROM 
            vendas v
        JOIN 
            produtos p ON v.nomeproduto = p.nomeproduto
        GROUP BY 
            v.nomeproduto
        ORDER BY 
            valor_total_venda DESC;
    '''
    resultados = hook.get_records(sql)
    colnames = ['nomeproduto', 'quantidade_total', 'valor_total_venda']
    caminho_arquivo = '/opt/airflow/leituraDevolvida/venda_produtos.csv'
    with open(caminho_arquivo, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(colnames)
        writer.writerows(resultados)

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2025, 9, 13),
    'retries': 1
}

with DAG(
    dag_id='group_by_vendas_produtos',
    default_args=default_args,
    schedule='@daily',
    catchup=False,
    max_active_runs=1
) as dag:
    salvar_task = PythonOperator(
        task_id='salvar_resultado',
        python_callable=salvar_resultado
    )
