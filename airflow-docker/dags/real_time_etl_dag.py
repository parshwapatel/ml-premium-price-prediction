from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from datetime import datetime

# Define your ETL functions
def extract_data_from_supabase():
    postgres_hook = PostgresHook(postgres_conn_id="supabase_connection")
    sql = "SELECT * FROM users;"
    records = postgres_hook.get_records(sql)
    return records

def transform_data(records):
    transformed_data = []
    for record in records:
        transformed_record = {
            'age': record[1],
            'number_of_dependants': record[2],
            'income_lakhs': record[3],
            'genetical_risk': record[4],
            'insurance_plan': record[5],
            'employment_status': record[6],
            'gender': record[7],
            'marital_status': record[8],
            'bmi_category': record[9],
            'smoking_status': record[10],
            'region': record[11],
            'medical_history': record[12]
        }
        transformed_data.append(transformed_record)
    return transformed_data

def load_data_to_api(transformed_data):
    # This function can call your API to load the transformed data
    pass

# Define the DAG for Airflow
dag = DAG(
    'real_time_etl_pipeline',
    default_args={'owner': 'airflow', 'start_date': datetime(2025, 1, 1), 'retries': 1},
    description='Real-time ETL pipeline for Supabase data',
    schedule='@hourly',
)

# Define the tasks using PythonOperator
extract_task = PythonOperator(
    task_id='extract_data',
    python_callable=extract_data_from_supabase,
    dag=dag,
)

transform_task = PythonOperator(
    task_id='transform_data',
    python_callable=transform_data,
    op_kwargs={'records': '{{ task_instance.xcom_pull(task_ids="extract_data") }}'},
    dag=dag,
)

load_task = PythonOperator(
    task_id='load_data',
    python_callable=load_data_to_api,
    op_kwargs={'transformed_data': '{{ task_instance.xcom_pull(task_ids="transform_data") }}'},
    dag=dag,
)

# Set the task dependencies
extract_task >> transform_task >> load_task
