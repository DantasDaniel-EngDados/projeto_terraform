from airflow import DAG
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.operators.python import PythonOperator
from datetime import datetime
import csv
import pandas as pd
import matplotlib.pyplot as plt
import os

def salvar_resultado():
    sql_file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../sql/salvar_resultado_csv_pdf.sql'))
    with open(sql_file_path, 'r', encoding='utf-8') as f:
        sql = f.read()
    
    hook = PostgresHook(postgres_conn_id='postgres_default')
    resultados = hook.get_records(sql)
    colnames = ['nomeproduto', 'quantidade_total', 'valor_total_venda', 'mes_venda', 'ano_venda']
    caminho_arquivo = '/tmp/venda_produtos.csv'
    with open(caminho_arquivo, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(colnames)
        writer.writerows(resultados)
    return caminho_arquivo

def gerar_grafico_pdf(**kwargs):
    ti = kwargs['ti']
    caminho_csv = ti.xcom_pull(task_ids='salvar_resultado')

    df = pd.read_csv(caminho_csv)

    df['mes_venda'] = df['mes_venda'].astype(int)
    df['ano_venda'] = df['ano_venda'].astype(int)
    df['data_mensal'] = pd.to_datetime(dict(year=df['ano_venda'], month=df['mes_venda'], day=1))

    meses_disponiveis = df['data_mensal'].unique()

    for data in meses_disponiveis:
        data_dt = pd.to_datetime(data)
        df_filtrado = df[df['data_mensal'] == data]

        caminho_pdf = f'/tmp/produto_valor_total_{data_dt.strftime("%Y_%m")}.pdf'

        fig, ax1 = plt.subplots(figsize=(12, 6))

        ax1.bar(df_filtrado['nomeproduto'], df_filtrado['quantidade_total'], color='b', alpha=0.6, label='Quantidade Total')
        ax1.set_xlabel('Produto')
        ax1.set_ylabel('Quantidade Total', color='b')
        ax1.tick_params(axis='y', labelcolor='b')
        plt.xticks(rotation=45, ha='right')

        ax2 = ax1.twinx()
        ax2.plot(df_filtrado['nomeproduto'], df_filtrado['valor_total_venda'], color='r', marker='o', label='Valor Total Venda')
        ax2.set_ylabel('Valor Total Venda', color='r')
        ax2.tick_params(axis='y', labelcolor='r')

        plt.title(f'Comparativo por Produto - Mês: {data_dt.strftime("%m/%Y")}')
        fig.tight_layout()

        plt.savefig(caminho_pdf)
        plt.close()

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2025, 9, 12),
    'retries': 1,
}

with DAG(
    dag_id='vendas_por_mes_multi_pdf',
    default_args=default_args,
    schedule='@daily',
    catchup=False,
    max_active_runs=1,
) as dag:

    salvar_task = PythonOperator(
        task_id='salvar_resultado',
        python_callable=salvar_resultado,
    )

    grafico_task = PythonOperator(
        task_id='gerar_grafico_pdf',
        python_callable=gerar_grafico_pdf,
    )

    salvar_task >> grafico_task
