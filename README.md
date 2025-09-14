Projeto de estudo onde o terraform inicia o banco de dados postgres e roda o airflow para executar as DAGs que alimentam os bancos de dados com as informações passadas pelo CSV. Logo após alimenta-los a DAG calcula_vendas_por_produtos cria um novo arquivo .csv fazendo GROUP BY entre os valores para trazer o resultado entre quantidade de vendas e valores totais recebidos, dentro do container para ser exportado para a pasta leituraDevolvida.

Usando venv:
    .\.venv\Scripts\Activate.ps1

Versão Python:
    Python version 3.10.0

Comandos para usar no venv: #OBS: Pode faltar algum comando ou ter mais que o necessário dependendo da máquina, mas tentei se o mais completo possível.
    pip install apache-airflow==2.10.0
    pip install -r requirements.txt  #lembrar de criar o requirements.txt com as bibliotecas nessesárias
    pip install --upgrade pip setuptools wheel
    pip install apache-airflow apache-airflow-providers-postgres

    No Power Shell:
        $env:AIRFLOW_VERSION="2.10.0"
        $env:PYTHON_VERSION="3.10.0"
        $env:CONSTRAINT_URL="https://raw.githubusercontent.com/apache/airflow/constraints-$($env:AIRFLOW_VERSION)/constraints-$($env:PYTHON_VERSION).txt"

        pip install apache-airflow==$env:AIRFLOW_VERSION --constraint $env:CONSTRAINT_URL
        pip install apache-airflow-providers-postgres --constraint $env:CONSTRAINT_URL

Para iniciar o terraform, na pasta terraform rodar os comando via power shell do venv:
    terraform init
    terraform apply
    terraform destroy

Para iniciar o airflow, na pasta airflow rodar os comando via power shell do venv:
    docker-compose build --no-cache
    docker-compose up airflow-init
    docker-compose up -d

Para verificar 
    docker exec -it postgres_local psql -U "Nome_do_usuario" -d "Nome_do_banco_de_dados"

Para copiar o .csv criado no container para dentro do leituraDevolvida:
    docker cp airflow-airflow-worker-1:/tmp/venda_produtos.csv ..\leituraDevolvida\venda_produtos.csv

arquivos a serem criados:
    /terraform/terraform.tfvars
        postgres_password = ""
        postgres_user     = ""
        postgres_db       = ""
        accept_eula = ""
        hostvar     = ""

        porta_interna = 
        porta_externa = 

    /terraform/variables.tf
        variable "porta_interna" {
        type    = number
        default = 5432
        }
        variable "porta_externa" {
        type    = number
        default = 5432
        }
        variable "postgres_password" {
        type      = string
        sensitive = true
        }
        variable "postgres_user" {
        type    = string
        default = "postgres"
        }
        variable "postgres_db" {
        type    = string
        default = "postgres"
        }
        variable "hostvar" {
        type    = string
        default = "postgres"
        }

Caso seja preciso estabelecer conexão do airflow com o banco de dados postgres criado pelo terraform:
    No UI do airflow:
        Admin -> Connections:
            conn_id: tente usar o => postgres_default
            #Não encontrei comandos para verificar isso via CMD que funcionaram