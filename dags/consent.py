from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.bash_operator import BashOperator
from airflow.operators.docker_operator import DockerOperator
from airflow.operators.python_operator import PythonOperator

from datetime import datetime, timedelta



def  validate_func():
#    import pandas
#    df=pandas.read_csv("/home/data",header=None)
#    df.columns=["first_name","last_name","email","dob","id","gender","colour","religion","civil_stand","number"]
#    df.to_csv("/usr/local/input/singhealth_dataset1.csv")
#    df.to_parquet("/usr/local/input/singhealth_dataset1.parquet")
    return 'completed validation'

def  updateconsent_func():
#    import pandas
#    df=pandas.read_csv("/home/data",header=None)
#    df.columns=["first_name","last_name","email","dob","id","gender","colour","religion","civil_stand","number"]
#    df.to_csv("/usr/local/input/singhealth_dataset1.csv")
#    df.to_parquet("/usr/local/input/singhealth_dataset1.parquet")
    return 'updated consent'


with DAG(dag_id='Consent_Test', schedule_interval="@once", start_date=datetime(2020, 1, 1), catchup=False) as dag:



    consent_test = DockerOperator(
        task_id='Consent_Test',
        api_version='auto',
        auto_remove=True,
        volumes=['/home/data:/data','/home/data/scripts:/scripts'], 
        docker_url="unix://var/run/docker.sock",
        network_mode="bridge",
        image='hadesfrontend',
        command= "python3 -O sand.py /data/europe/Europe_ZoneA_Data_Input.parq /data/demo1/DeID_Europe_ZoneA_Data_Input1.parq /scripts/d.yaml  -pack 10000 -logfile /data/europe/europe_to_japan_zone1.log"
        )

consent_test
