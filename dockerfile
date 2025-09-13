FROM apache/airflow:3.0.2

USER root

# Cria diretório e instala redis-tools
RUN mkdir -p /opt/airflow/leituras && \
    mkdir -p /opt/sql && \
    mkdir -p /tmp && \
    mkdir -p /opt/airflow/leituraDevolvida && \
    apt-get update && \
    apt-get install -y redis-tools && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

    COPY ./leituras/produtos_adicionados.csv /opt/airflow/leituras
    COPY ./leituras/vendas_adicionadas.csv /opt/airflow/leituras
    COPY ./sql/init.sql /opt/sql


USER airflow
