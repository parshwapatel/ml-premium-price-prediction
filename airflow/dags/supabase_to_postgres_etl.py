from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from database1.database_ext import save_user_data_to_supabase  # Import the Supabase extraction function
from database1.database_load import save_user_data_to_postgres  # Import the PostgreSQL load function
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.hooks.base import BaseHook
from supabase import create_client, Client
import os

# Fetch Supabase credentials from environment variables
supabase_url = os.getenv('SUPABASE_URL')  # Make sure this is set in your environment
supabase_key = os.getenv('SUPABASE_KEY')  # Make sure this is set in your environment

# Initialize Supabase client
supabase_client: Client = create_client(supabase_url, supabase_key)

# Define the DAG
dag = DAG(
    dag_id='supabase_to_postgres_etl',
    description='ETL pipeline to move data from Supabase to PostgreSQL with transformations',
    schedule_interval='@hourly',  # Modify as needed (this runs hourly)
    start_date=datetime(2025, 2, 25),
    catchup=False
)

# Task to extract data from Supabase
def extract_data_from_supabase():
    # Fetch the data from Supabase (this will be used to pass to the next task)
    response = supabase_client.table("users").select("*").execute()
    return response.data  # Return the data to be passed to the next task


# Task to transform data (Example: subtract 2 from the 'id' column)
def transform_data(**kwargs):
    # Pull data from the previous task
    data = kwargs['ti'].xcom_pull(task_ids='extract_data')
    transformed_data = []
    
    # Perform transformations on the data
    for row in data:
        transformed_row = row.copy()  # Create a copy of the row
        transformed_row['id'] = row['id'] - 2  # Example transformation (subtract 2 from 'id')
        transformed_data.append(transformed_row)
    
    return transformed_data


# Task to load data into PostgreSQL
def load_data_to_postgresql(**kwargs):
    # Pull transformed data from the previous task
    data = kwargs['ti'].xcom_pull(task_ids='transform_data')

    # Get the connection using the Airflow connection ID
    postgres_hook = PostgresHook(postgres_conn_id='postgres_conn')
    conn = postgres_hook.get_conn()
    cursor = conn.cursor()
    
    # Insert each row into PostgreSQL using the save_user_data_to_postgres function
    for row in data:
        save_user_data_to_postgres(
            row['age'],
            row['number_of_dependants'],
            row['income_lakhs'],
            row['genetical_risk'],
            row['insurance_plan'],
            row['employment_status'],
            row['gender'],
            row['marital_status'],
            row['bmi_category'],
            row['smoking_status'],
            row['region'],
            row['medical_history']
        )

    conn.commit()
    cursor.close()
    conn.close()


# Define the tasks
extract_task = PythonOperator(
    task_id='extract_data',
    python_callable=extract_data_from_supabase,
    dag=dag
)

transform_task = PythonOperator(
    task_id='transform_data',
    python_callable=transform_data,
    provide_context=True,  # Ensure that context is passed so XCom can work
    dag=dag
)

load_task = PythonOperator(
    task_id='load_data',
    python_callable=load_data_to_postgresql,
    provide_context=True,  # Ensure that context is passed so XCom can work
    dag=dag
)

# Set task dependencies
extract_task >> transform_task >> load_task
