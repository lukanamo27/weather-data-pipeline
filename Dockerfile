FROM apache/airflow:2.7.3

USER root
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt
USER airflow
