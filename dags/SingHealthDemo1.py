from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.bash_operator import BashOperator
from airflow.operators.docker_operator import DockerOperator
from airflow.operators.python_operator import PythonOperator

from datetime import datetime, timedelta

def  convert_csv_func():
    print('Fixup CSV to parquet')
    import pandas
    #df=pandas.read_csv("/usr/local/input/singhealth_dataset.csv",header=None)
    df=pandas.read_csv("/usr/local/input/singhealth_dataset.csv",header=0)
    #df.columns=["NRIC,first_name","last_name","email","dob","id","gender","colour","religion","civil_stand","number"]
    #df.to_csv("/usr/local/input/singhealth_dataset1.csv")
    df.to_parquet("/usr/local/input/singhealth_dataset1.parquet")
    return 'completed csv fixup'

def  tokenize_csv_func():
    return 'completed masking'

def  mask_csv_func():
    return 'completed masking'

def  export_csv_func():
    return 'completed export'

with DAG(dag_id='singhealth_dag', schedule_interval="@once", start_date=datetime(2020, 1, 1), catchup=False) as dag:

    check_input = BashOperator(task_id='check_csv_input', bash_command='id')

    handle_csv = PythonOperator(task_id='convert_csv', python_callable=convert_csv_func)

#    tokenize_csv= PythonOperator(task_id='tokenize_csv', python_callable=tokenize_csv_func)

    mask_csv= PythonOperator(task_id='mask_csv', python_callable=mask_csv_func)

    export_csv= PythonOperator(task_id='export_csv', python_callable=export_csv_func)


    tokenize_csv= DockerOperator(
        task_id='docker_command',
        image='res-drl-docker-local.artifactory.swg-devops.com/dpt/base-cli',
        api_version='auto',
        auto_remove=True,
        command="",
        volumes=['/usr/local/input/:/input','/usr/local/input/:/config','/usr/local/output/:/output'], 
        docker_url="unix://var/run/docker.sock",
        network_mode="bridge"
        )

 #   tokenize_csv= DockerOperator(
 #       task_id='docker_command',
 #       image='hades26',
 #       api_version='auto',
 #       auto_remove=True,
 #       command="/home/hades/cbin/run.sh -g 0 -G25000 test_example30.csv test_policy.yaml",
 #       docker_url="unix://var/run/docker.sock",
 #       network_mode="bridge"
 #       )


    check_input >> handle_csv >> tokenize_csv >> mask_csv >> export_csv
