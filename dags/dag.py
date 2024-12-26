import sys
import os
import django
from datetime import datetime, timedelta
import random
import requests
import logging
from croniter import croniter, CroniterBadCronError
from airflow import DAG
from airflow.operators.python import PythonOperator

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Set the path to your Django project
sys.path.append('/mnt/e/GS/Airflow/simulator_project')  
os.environ['DJANGO_SETTINGS_MODULE'] = 'simulator_project.settings' 
django.setup()

# Now you can import your models after setting up Django
from simulators.models import Simulator

def validate_cron(cron_expression):
    """Validate a cron expression."""
    try:
        croniter(cron_expression)
        return True
    except CroniterBadCronError:
        return False

def generate_value():
    return random.uniform(1, 100)

def call_kpi_endpoint(value, kpi_id):
    try:
        response = requests.post(
            'http://localhost:8000/api/calculate-kpi/',
            json={'value': value, 'kpi_id': kpi_id}
        )
        response.raise_for_status()  
        return response.json().get('result', None)
    except requests.RequestException as e:
        logger.error(f"Error calling KPI endpoint: {e}")
        return None

def process_kpi(**context):
    value = generate_value()
    kpi_id = context['params']['kpi_id']
    result = call_kpi_endpoint(value, kpi_id)
    if result is not None:
        logger.info(f"Value: {value}, KPI {kpi_id} result: {result}")
    else:
        logger.error(f"Failed to get result for KPI {kpi_id} with value {value}")

# Fetch simulators from Django
simulators = Simulator.objects.all()

for simulator in simulators:
    logger.info(f"Simulator ID: {simulator.id}, Interval: {simulator.interval}")

    dag_id = f'kpi_simulator_{simulator.id}'

    if isinstance(simulator.start_date, str):
        start_date = datetime.strptime(simulator.start_date, '%b. %d, %Y, midnight')
    else:
        start_date = simulator.start_date  

    # Validate and set the schedule_interval
    if isinstance(simulator.interval, timedelta):
        schedule_interval = simulator.interval
    elif isinstance(simulator.interval, str):
        if validate_cron(simulator.interval):
            schedule_interval = simulator.interval
        else:
            logger.error(f"Invalid cron expression for simulator {simulator.id}: {simulator.interval}")
            continue  # Skip invalid cron expressions
    else:
        logger.error(f"Invalid schedule_interval format for simulator {simulator.id}: {simulator.interval}")
        continue

    default_args = {
        'owner': 'airflow',
        'start_date': start_date,  # Use the parsed start_date
        'depends_on_past': False,
        'retries': 1,
    }

    # Create the DAG
    dag = DAG(
        dag_id,
        default_args=default_args,
        schedule_interval=schedule_interval,
        catchup=False
    )

    # Add the task to the DAG
    with dag:
        task = PythonOperator(
            task_id='process_kpi',
            python_callable=process_kpi,
            op_kwargs={'kpi_id': simulator.kpi_id},
            params={'kpi_id': simulator.kpi_id}
        )

    globals()[dag_id] = dag
    logger.info(f"DAG {dag_id} created successfully.")