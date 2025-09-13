Usando venv
.\.venv\Scripts\Activate.ps1

Python version 3.10.0

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


terraform init
terraform apply
terraform destroy

docker-compose build --no-cache
docker-compose up airflow-init
docker-compose up -d

docker exec -it postgres_local psql -U postgres -d postgres