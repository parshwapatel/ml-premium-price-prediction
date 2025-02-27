from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from database.database import save_user_data_to_supabase  # Import the function

# Define the DAG
dag = DAG(
    'supabase_etl_pipeline',
    description='ETL pipeline for Supabase data with transformation',
    schedule_interval='@daily',  # Modify as needed
    start_date=datetime(2025, 2, 25),
    catchup=False
)

# Task to extract data from Supabase
def extract_data_from_supabase():
    response = supabase.table('users').select('*').execute()
    return response.data

# Task to transform data (subtract 2 from 'id' column)
def transform_data(data):
    transformed_data = []
    for row in data:
        transformed_row = row.copy()  # Create a copy of the row to avoid modifying the original
        transformed_row['id'] = row['id'] - 2  # Subtract 2 from the 'id' column
        transformed_data.append(transformed_row)
    return transformed_data

# Task to load data into Supabase
def load_data_to_supabase(data):
    for row in data:
        save_user_data_to_supabase(
            row['id'],  # Ensure to include the transformed 'id' here
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

# Define the tasks
extract_task = PythonOperator(
    task_id='extract_data',
    python_callable=extract_data_from_supabase,
    dag=dag
)

transform_task = PythonOperator(
    task_id='transform_data',
    python_callable=transform_data,
    op_args=['{{ task_instance.xcom_pull(task_ids="extract_data") }}'],
    dag=dag
)

load_task = PythonOperator(
    task_id='load_data',
    python_callable=load_data_to_supabase,
    op_args=['{{ task_instance.xcom_pull(task_ids="transform_data") }}'],
    dag=dag
)

# Set task dependencies
extract_task >> transform_task >> load_task
