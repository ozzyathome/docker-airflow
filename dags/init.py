import uuid
from datetime import datetime
from airflow import DAG
from airflow.utils.trigger_rule import TriggerRule
from airflow.operators.postgres_operator import PostgresOperator
from airflow.operators.dummy_operator import DummyOperator

dag_params = {
    'dag_id': 'Init_Demo_Daga',
    'template_searchpath': '/opt/airflow/sql',
    'start_date': datetime(2020, 10, 7),
    'schedule_interval': None
}


with DAG(**dag_params) as dag:

    start = DummyOperator(
            task_id = 'start')

    init_demo = PostgresOperator(
        postgres_conn_id='postgres_data',
        task_id = 'init_demo',
        sql = ['init_honda_demo.sql'],
        autocommit = True)


start >> init_demo
