import uuid
from datetime import datetime
from airflow import DAG
from airflow.utils.trigger_rule import TriggerRule
from airflow.operators.postgres_operator import PostgresOperator


dag_params = {
    'dag_id': 'PostgresOperator_dag',
    'start_date': datetime(2020, 10, 7),
    'schedule_interval': None
}


with DAG(**dag_params) as dag:


    drop_europe_consent_table = PostgresOperator(
        postgres_conn_id='postgres_data',
        task_id='drop_consent_table_europe',
        sql='''DROP TABLE IF EXISTS consent_europe(
            );''',
    )

    create_europe_consent_table = PostgresOperator(
        postgres_conn_id='postgres_data',
        task_id='create_consent_table_europe',
        sql='''CREATE TABLE IF NOT EXISTS consent_europe(
            email TEXT NOT NULL, consent char NOT NULL 
            );''',
    )

    drop_japan_consent_table = PostgresOperator(
        postgres_conn_id='postgres_data',
        task_id='drop_consent_table_japan',
        sql='''DROP TABLE IF EXISTS consent_europe
            ;''',
    )

    create_japan_consent_table = PostgresOperator(
        postgres_conn_id='postgres_data',
        task_id='create_consent_table_japan',
        sql='''CREATE TABLE IF NOT EXISTS consent_europe(
            email TEXT NOT NULL, consent char NOT NULL 
            );''',
    )


    insert_europe_consent = PostgresOperator(
        task_id='insert_row',
        postgres_conn_id='postgres_data',
        sql="""
		INSERT INTO consent_europe VALUES('123@zurich.ibm.com','y');
                INSERT INTO consent_europe VALUES('234@zurich.ibm.com','n');
                INSERT INTO consent_europe VALUES('345@zurich.ibm.com','y');
                INSERT INTO consent_europe VALUES('4123@zurich.ibm.com','y');
                INSERT INTO consent_europe VALUES('13323@zurich.ibm.com','y');
                INSERT INTO consent_europe VALUES('122223@zurich.ibm.com','y');
		""", 
)

    drop_europe_consent_table >> create_europe_consent_table >> insert_europe_consent  
    drop_japan_consent_table >>  create_japan_consent_table
