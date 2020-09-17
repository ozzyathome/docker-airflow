import os

from airflow import DAG 
from airflow.plugins_manager import AirflowPlugin

#import airflow.plugins.operators as operators
from airflow.operators.python_operator import PythonOperator
from airflow.operators.dagrun_operator import TriggerDagRunOperator 
from airflow.operators import OmegaFileSensor, ArchiveFileOperator
from airflow.operators import FileSensor1
from airflow_fs.operators import CopyFileOperator
from datetime import datetime, timedelta 
from airflow.models import Variable 
import logging
 
default_args = { 
    'owner': 'osb', 
    'depends_on_past': False, 
    'start_date': datetime(2017, 6, 26), 
    'provide_context': True, 
    'retries': 100, 
    'retry_delay': timedelta(seconds=30) 
    } 


filepath="/usr/local/input/"
filepattern="*.csv)"
archivepath='/usr/local/output'

task_name = 'file_sensor_task' 
#filepath = Variable.get("souPath") 
#filepattern = Variable.get("filePattern") 
#archivepath = Variable.get("archivePath") 
uploadPath= '/usr/local/input/*.csv'

dag = DAG(
    'task_name', 
    default_args=default_args, 
    schedule_interval=None, 
    catchup=False, 
    max_active_runs=1, 
    concurrency=1) 


sensor_task = FileSensor1(
    task_id='sensor_file',
    filepath=uploadPath,
    fs_conn_id='airflow_db',
    dag=dag,
)

def process_file(**context): 
    file_to_process = context['task_instance'].xcom_pull(key='file_name', task_ids='sensor_file') 
    LOGGER = logging.getLogger("airflow.task")

    LOGGER.info("FILE :" + file_to_process)
    LOGGER.info("FILE PATH:" + filepath)
    os.rename(file_to_process, archivepath)

    
 #   file = open(file_to_process, 'w') 
 #   file.write('This is a test\n') 
 #   file.write('of processing the file') 
 #   file.close() 




proccess_task = PythonOperator(
    task_id='process_the_file', python_callable=process_file, dag=dag) 

archive_task = ArchiveFileOperator(
    task_id='archive_file', 
    filepath=filepath, 
    task_name=task_name, 
    archivepath=archivepath, 
    dag=dag) 

trigger = TriggerDagRunOperator(
    task_id='trigger_dag_rerun', trigger_dag_id=task_name, dag=dag) 

sensor_task >> proccess_task >> archive_task >> trigger 