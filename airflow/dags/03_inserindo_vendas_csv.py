from airflow.decorators import dag, task
import psycopg2
import csv
import configPy

@dag(schedule='@daily', catchup=False, tags=['example'])
def importar_vendas_csv():

    @task()
    def inserir_dados_csv(caminho_csv):
        conn = psycopg2.connect(
            dbname=configPy.dbname, 
            user=configPy.user, 
            password=configPy.password, 
            host=configPy.host, 
            port=configPy.port
        )
        cur = conn.cursor()
        with open(caminho_csv, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader)  # pular cabeçalho
            for row in reader:
                cur.execute(
                    "INSERT INTO vendas (nomeproduto, quantidade, datavenda) VALUES (%s, %s, %s)",
                    row
                )
        conn.commit()
        cur.close()
        conn.close()

    caminho_csv = "/opt/airflow/leituras/vendas_adicionadas.csv"
    inserir_dados_csv(caminho_csv)

dag = importar_vendas_csv()
