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
    
    COPY ./leituras/produtos_adicionados.json /opt/airflow/leituras
    COPY ./leituras/vendas_adicionadas.json /opt/airflow/leituras
    COPY ./sql/init.sql /opt/sql
    COPY ./sql/group_by.sql /opt/sql
    COPY ./sql/inserindo_produtos_csv.sql /opt/sql
    COPY ./sql/inserindo_vendas_csv.sql /opt/sql


USER airflow

RUN pip install matplotlib pandas
