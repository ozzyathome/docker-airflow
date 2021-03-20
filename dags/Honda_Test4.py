from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.bash_operator import BashOperator
from airflow.contrib.sensors.file_sensor import FileSensor

from datetime import datetime, timedelta

import airflow

uploadPath= '/usr/local/input/'


default_args = {
    "depends_on_past" : False,
    "start_date"      : airflow.utils.dates.days_ago( 1 ),
    "retries"         : 1,
}

with DAG( "Honda_Test_4", default_args= default_args, schedule_interval= "@once"  ) as dag:

 #   sensor_task = FileSensor( task_id= "my_file_sensor_task", poke_interval= 30, filepath= "/usr/local/input/")


    command_dicom_prep = """
    sh /usr/local/hades/command_prep.sh;
    """
    bash_dicom_prepare = BashOperator(task_id='bash_dicom_prepare', bash_command=command_dicom_prep)

    command_dicom_split = """
    sh /usr/local/hades/command_split.sh;
    """

    bash_dicom_split = BashOperator(task_id='bash_dicom_split', bash_command=command_dicom_split)


    command_dicom_image = """
    sh /usr/local/hades/command_dicom_image.sh;
    """
    bash_dicom_image = BashOperator(task_id='bash_dicom_image', bash_command=command_dicom_image)

    command_dicom_meta = """
    sh /usr/local/hades/command_dicom_meta.sh;
    """
    bash_dicom_meta = BashOperator(task_id='bash_dicom_meta', bash_command=command_dicom_meta)

    command_dicom_merge = """
    sh /usr/local/hades/command_dicom_merge.sh;
    """
    bash_dicom_merge = BashOperator(task_id='bash_dicom_merge', bash_command=command_dicom_merge)


    bash_dicom_prepare >> bash_dicom_split >>  [ bash_dicom_image, bash_dicom_meta]  >>  bash_dicom_merge
  
