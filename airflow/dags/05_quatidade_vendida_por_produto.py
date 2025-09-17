from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt

def gerar_grafico_pdf():
    caminho_csv = '/tmp/venda_produtos.csv'
    caminho_pdf = '/tmp/produto_valor_total.pdf'

    df = pd.read_csv(caminho_csv)

    fig, ax1 = plt.subplots(figsize=(10, 6))

    ax1.bar(df['nomeproduto'], df['quantidade_total'], color='b', alpha=0.6, label='Quantidade Total')
    ax1.set_xlabel('Produto')
    ax1.set_ylabel('Quantidade Total', color='b')
    ax1.tick_params(axis='y', labelcolor='b')
    plt.xticks(rotation=45, ha='right')

    ax2 = ax1.twinx()
    ax2.plot(df['nomeproduto'], df['valor_total_venda'], color='r', marker='o', label='Valor Total Venda')
    ax2.set_ylabel('Valor Total Venda', color='r')
    ax2.tick_params(axis='y', labelcolor='r')

    plt.title('Comparativo entre Quantidade Total e Valor Total de Venda por Produto')
    fig.tight_layout()

    plt.savefig(caminho_pdf)

    plt.close()

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2025, 9, 16),
    'retries': 1
}

with DAG(
    dag_id='gera_grafico_venda_produtos',
    default_args=default_args,
    schedule='@daily',
    catchup=False,
    max_active_runs=1
) as dag:
    grafico_task = PythonOperator(
        task_id='gerar_grafico_pdf',
        python_callable=gerar_grafico_pdf
    )
