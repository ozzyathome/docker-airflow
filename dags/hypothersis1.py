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


with DAG(dag_id='1_Consent_Europe_To_Japan', schedule_interval="@once", start_date=datetime(2020, 1, 1), catchup=False) as dag:


    consent_csv= PythonOperator(task_id='update_consent', python_callable=updateconsent_func)

    validate1_csv= PythonOperator(task_id='validate_and_load_Japan_Zone1', python_callable=validate_func)

    validate2_csv= PythonOperator(task_id='validate_and_load_Japan_Zone2', python_callable=validate_func)

    data_to_japan_zone1 = DockerOperator(
        task_id='Data_To_Japan_Zone1',
        api_version='auto',
        auto_remove=True,
        volumes=['/home/data:/data','/home/data/scripts:/scripts'], 
        docker_url="unix://var/run/docker.sock",
        network_mode="bridge",
        image='hadesfrontend',
        command= "python3 -O sand.py /data/europe/Europe_ZoneA_Data_Input.parq /data/demo1/DeID_Europe_ZoneA_Data_Input1.parq /scripts/europe_to_japan_zone1.yaml  -pack 10000 -logfile /data/europe/europe_to_japan_zone1.log"
        )
 
    data_to_japan_zone2 = DockerOperator(
        task_id='Data_To_Japan_Zone_2',
        api_version='auto',
        auto_remove=True,
        volumes=['/home/data:/data','/home/data/scripts:/scripts'], 
        docker_url="unix://var/run/docker.sock",
        network_mode="bridge",
        image='hadesfrontend',
        command= "python3 -O sand.py /data/europe/Europe_ZoneA_Data_Input.parq /data/demo1/DeID_Europe_ZoneA_Data_Input2.parq /scripts/europe_to_japan_zone2.yaml  -pack 10000 -logfile /data/europe/europe_to_japan_zone2.log"
        )

    consent_csv >> data_to_japan_zone1  >> validate1_csv 
    consent_csv >> data_to_japan_zone2  >> validate2_csv

