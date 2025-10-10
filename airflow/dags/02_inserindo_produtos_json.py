import os
from airflow import DAG
from airflow.decorators import task
from datetime import datetime, timedelta
import psycopg2
import json

import configPy

DATA_PATH = "/mnt/leituras"
PROCESSED_FILE = "/tmp/processed_files_produtos.txt"
SQL_FILE_PATH = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../sql/inserindo_produtos_csv.sql"))

default_args = {
    "owner": "você",
    "retries": 0,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    "inserindo_produtos_json",
    default_args=default_args,
    description="Processa arquivos JSON de produtos não processados e insere no banco",
    schedule="@daily",
    start_date=datetime(2025, 8, 20),
    catchup=False,
    max_active_runs=1,
) as dag:

    @task
    def criar_arquivo_controle():
        if not os.path.exists(PROCESSED_FILE):
            with open(PROCESSED_FILE, "w") as f:
                f.write("")

    @task
    def listar_novos_arquivos():
        all_files = [os.path.join(DATA_PATH, fname)
                     for fname in os.listdir(DATA_PATH)
                     if fname.startswith("produtos") and fname.endswith(".json")]
        processed = set()
        if os.path.isfile(PROCESSED_FILE):
            with open(PROCESSED_FILE, "r") as f:
                processed = set(line.strip() for line in f if line.strip())
        novos = [f for f in all_files if f not in processed]
        return novos

    @task
    def extrair_transformar(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data

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
            cursor.execute(insert_query, (row["nomeproduto"], row["categoria"], row["preco"]))
        conn.commit()
        cursor.close()
        conn.close()

    @task
    def marcar_como_processado(file_path):
        with open(PROCESSED_FILE, "a") as f:
            f.write(f"{file_path}\n")

    criar_arquivo_controle_task = criar_arquivo_controle()
    arquivos_novos = listar_novos_arquivos()
    arquivos_novos.set_upstream(criar_arquivo_controle_task)

    # Dynamic task mapping
    dados = extrair_transformar.expand(file_path=arquivos_novos)
    dados.set_upstream(arquivos_novos)
    carregar.expand(dados=dados)
    marcar_como_processado.expand(file_path=arquivos_novos)
