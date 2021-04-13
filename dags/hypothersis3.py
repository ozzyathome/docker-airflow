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



with DAG(dag_id='3_Reidentification', schedule_interval="@once", start_date=datetime(2020, 1, 1), catchup=False) as dag:


    reid_csv= PythonOperator(task_id='reidentify', python_callable=reidentify_func)

    data_to_japan_zone1 = DockerOperator(
        task_id='Data_To_Europe',
        api_version='auto',
        auto_remove=True,
        volumes=['/home/data:/data','/home/data/scripts:/scripts'], 
        docker_url="unix://var/run/docker.sock",
        network_mode="bridge",
        image='hadesfrontend',
        command= "python3 -O sand.py /data/europe/Europe_ZoneA_Data_Input.parq /data/japan/Zone1/DeID_Europe_ZoneA_Data_Input.parq /scripts/europe_to_japan_zone1.yaml  -pack 10000 -logfile /data/europe/europe_to_japan_zone1.log"
        )
 
    data_to_japan_zone1   >> reid_csv

