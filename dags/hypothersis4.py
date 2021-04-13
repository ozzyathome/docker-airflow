from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.bash_operator import BashOperator
from airflow.operators.docker_operator import DockerOperator
from airflow.operators.python_operator import PythonOperator

from datetime import datetime, timedelta



def  reidentify_func():
#    import pandas
#    df=pandas.read_csv("/home/data",header=None)
#    df.columns=["first_name","last_name","email","dob","id","gender","colour","religion","civil_stand","number"]
#    df.to_csv("/usr/local/input/singhealth_dataset1.csv")
#    df.to_parquet("/usr/local/input/singhealth_dataset1.parquet")
    return 'completed masking'


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


with DAG(dag_id='4_Regional_Policies', schedule_interval="@once", start_date=datetime(2020, 1, 1), catchup=False) as dag:

    consent_csv= PythonOperator(task_id='update_consent', python_callable=updateconsent_func)

    validate1_csv= PythonOperator(task_id='validate_and_load_us_Japan_Zone3', python_callable=validate_func)

    validate2_csv= PythonOperator(task_id='validate_and_load_eu_Japan_Zone3', python_callable=validate_func)


    us_data_to_japan_zone2 = DockerOperator(
        task_id='US_Data_To_Japan_Zone3',
        api_version='auto',
        auto_remove=True,
        volumes=['/home/data:/data','/home/data/scripts:/scripts'], 
        docker_url="unix://var/run/docker.sock",
        network_mode="bridge",
        image='hadesfrontend',
        command= "python3 -O sand.py /data/us/US_ZoneA_Data_Input.parq /data/demo4/DeID_US_ZoneA_Data_Input.parq /scripts/us_to_japan_zone2.yaml  -pack 10000 -logfile /data/us/us_to_japan_zone2.log"
        )
 
    europe_data_to_japan_zone2 = DockerOperator(
        task_id='Europe_Data_To_Japan_Zone3',
        api_version='auto',
        auto_remove=True,
        volumes=['/home/data:/data','/home/data/scripts:/scripts'], 
        docker_url="unix://var/run/docker.sock",
        network_mode="bridge",
        image='hadesfrontend',
        command= "python3 -O sand.py /data/europe/Europe_ZoneA_Data_Input.parq /data/demo4/DeID_Europe_ZoneA_Data_Input.parq /scripts/europe_to_japan_zone2.yaml  -pack 10000 -logfile /data/europe/europe_to_japan_zone2.log"
        )

    consent_csv >> us_data_to_japan_zone2 >> validate1_csv  
    consent_csv >> europe_data_to_japan_zone2  >> validate2_csv


