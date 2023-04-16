from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator


default_args = {
    'owner': 'yourname',
    'depends_on_past': False,
    'start_date': datetime(2023, 3, 27),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'air_quality_pipeline',
    default_args=default_args,
    description='Air quality data streaming pipeline',
    schedule_interval='@daily',
)

# Task to run producer.py
t1 = BashOperator(
    task_id='run_producer',
    bash_command='python3 "/Users/srivardhan/Desktop/Masters/Masters Project/Kafka Implementation/kafka-pipeline-examples/producer-consumer/producer.py"',
    dag=dag,
)

# Task to run consumer.py
t2 = BashOperator(
    task_id='run_consumer',
    bash_command='python3 "/Users/srivardhan/Desktop/Masters/Masters Project/Kafka Implementation/kafka-pipeline-examples/producer-consumer/consumer.py"',
    dag=dag,
)

# Define the task dependencies
t1 >> t2 
