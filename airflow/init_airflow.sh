#!/bin/bash
set -e
airflow db migrate
airflow users create \
  --username "${AIRFLOW_ADMIN_USERNAME}" \
  --firstname "${AIRFLOW_ADMIN_FIRSTNAME}" \
  --lastname "${AIRFLOW_ADMIN_LASTNAME}" \
  --email "${AIRFLOW_ADMIN_EMAIL}" \
  --password "${AIRFLOW_ADMIN_PASSWORD}" \
  --role Admin
