import os
from airflow import DAG
from airflow.decorators import task
from datetime import datetime, timedelta
import pandas as pd
import psycopg2

import configPy

DATA_PATH = "/opt/airflow/leituras"
FILE_NAME = "vendas_adicionadas.csv"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SQL_FILE_PATH = os.path.abspath(os.path.join(BASE_DIR, "../../sql/inserindo_vendas_csv.sql"))

default_args = {
    "owner": "você",
    "retries": 0,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    "inserindo_vendas_csv",
    default_args=default_args,
    description="Insere dados informados no banco de dados",
    schedule="@daily",
    start_date=datetime(2025, 8, 20),
    catchup=False
) as dag:

    @task
    def verificar_arquivo():
        file_path = os.path.join(DATA_PATH, FILE_NAME)
        if os.path.isfile(file_path):
            print(f"Arquivo encontrado: {file_path}")
            return file_path
        else:
            raise FileNotFoundError(f"Arquivo {file_path} não encontrado")

    @task
    def extrair_transformar(file_path):
        print(f"Lendo arquivo: {file_path}")
        df = pd.read_csv(file_path)
        df["datavenda"] = pd.to_datetime(df["datavenda"]).dt.date
        return df.to_dict(orient="records")

    @task
    def carregar(dados):
        with open(SQL_FILE_PATH, "r") as f:
            insert_query = f.read()
        conn = psycopg2.connect(
            dbname=configPy.dbname,
            user=configPy.user,
            password=configPy.password,
            host=configPy.host,
            port=configPy.port 
        )
        cursor = conn.cursor()
        for row in dados:
            cursor.execute(insert_query, (row["nomeproduto"], row["quantidade"], row["datavenda"]))
        conn.commit()
        cursor.close()
        conn.close()

    arquivo = verificar_arquivo()
    dados_diarios = extrair_transformar(arquivo)
    carregar(dados_diarios)