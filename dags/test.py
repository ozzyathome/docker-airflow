from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.bash_operator import BashOperator
from airflow.operators.docker_operator import DockerOperator
from airflow.operators.python_operator import PythonOperator

from datetime import datetime, timedelta



def  mask_csv_func():
#    import pandas
#    df=pandas.read_csv("/home/data",header=None)
#    df.columns=["first_name","last_name","email","dob","id","gender","colour","religion","civil_stand","number"]
#    df.to_csv("/usr/local/input/singhealth_dataset1.csv")
#    df.to_parquet("/usr/local/input/singhealth_dataset1.parquet")
    return 'completed masking'

with DAG(dag_id='container_test_dag', schedule_interval="@once", start_date=datetime(2020, 1, 1), catchup=False) as dag:


    mask_csv= PythonOperator(task_id='mask_csv', python_callable=mask_csv_func)

    tokenize_parq= DockerOperator(
        task_id='hades_docker_command',
        image='hadesv26',
        api_version='auto',
        auto_remove=False,
        tty=True,
        environment={
           'AF_EXECUTION_DATE': "{{ ds }}",
           'AF_OWNER': "{{ task.owner }}"
        },
#       command='/bin/bash -c \'echo "TASK ID (from macros): {{ task.task_id }} - EXECUTION DATE (from env vars): $AF_EXECUTION_DATE"\'',
        command="bash -c 'cd /home/hades; python3 -O sand.py /home/data/test.parq /home/data/testresult.parq email.yaml -pack 10000 -logfile ../data/testynrg_osb.log'", 
        volumes=['/Users/osb/git/airflow/input:/home/data'],
        docker_url="tcp://socat:2375",
        network_mode="bridge"
        )

    tokenize_parq >> mask_csv

