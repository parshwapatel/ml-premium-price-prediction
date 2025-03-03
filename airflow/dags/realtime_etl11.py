from airflow import DAG
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.operators.python import PythonOperator
import requests
import pendulum

# Define the DAG
dag = DAG(
    'realtime_etl11',
    description='Extract data from Supabase, Transform (id - 2), and Load into PostgreSQL',
    schedule ='@hourly',  # You can adjust the interval as needed
    start_date = pendulum.today('UTC').subtract(days=1),
    catchup=False,
)

# --- Extract Data from Supabase ---
def extract_data_from_supabase(**kwargs):
    url = 'https://vndclryqjcrarvhtpfrf.supabase.co/rest/v1/users?select=*'
    headers = {
        "apikey": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZuZGNscnlxamNyYXJ2aHRwZnJmIiwicm9sZSI6ImFub24iLCJpYXQiOjE3Mzk3NDgwMDUsImV4cCI6MjA1NTMyNDAwNX0.LWu2AU3iJHZNCyHBw_1j-nh4yZBLop7PKShrr599OqU",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZuZGNscnlxamNyYXJ2aHRwZnJmIiwicm9sZSI6ImFub24iLCJpYXQiOjE3Mzk3NDgwMDUsImV4cCI6MjA1NTMyNDAwNX0.LWu2AU3iJHZNCyHBw_1j-nh4yZBLop7PKShrr599OqU"
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        extracted_data = response.json()
        kwargs['ti'].xcom_push(key='extracted_data', value=extracted_data)  # Store data in XCom
    else:
        raise ValueError(f"Error fetching data: {response.status_code}")

# --- Transform the Data ---
def transform_data(**kwargs):
    ti = kwargs['ti']
    extracted_data = ti.xcom_pull(task_ids='extract_data_from_supabase', key='extracted_data')

    transformed_data = []
    for record in extracted_data:
        transformed_record = {
            "id": record.get("id", 0) - 2,  # Avoid None values
            "age": record.get("age"),
            "number_of_dependants": record.get("number_of_dependants"),
            "income_lakhs": record.get("income_lakhs"),
            "genetical_risk": record.get("genetical_risk"),
            "insurance_plan": record.get("insurance_plan"),
            "employment_status": record.get("employment_status"),
            "gender": record.get("gender"),
            "marital_status": record.get("marital_status"),
            "bmi_category": record.get("bmi_category"),
            "smoking_status": record.get("smoking_status"),
            "region": record.get("region"),
            "medical_history": record.get("medical_history"),
        }
        transformed_data.append(transformed_record)

    ti.xcom_push(key='transformed_data', value=transformed_data)  # Store transformed data in XCom

# --- Load Data into PostgreSQL ---
def load_data_to_postgres(**kwargs):
    ti = kwargs['ti']
    transformed_data = ti.xcom_pull(task_ids='transform_data', key='transformed_data')

    postgres_conn_id = 'pgadmin4_conn'
    sql = """
        INSERT INTO users (id, age, number_of_dependants, income_lakhs, genetical_risk, 
                           insurance_plan, employment_status, gender, marital_status, bmi_category, 
                           smoking_status, region, medical_history)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    postgres_hook = PostgresHook(postgres_conn_id=postgres_conn_id)
    connection = postgres_hook.get_conn()
    cursor = connection.cursor()

    # Insert data in batch
    batch_values = [
        (record['id'], record['age'], record['number_of_dependants'], record['income_lakhs'],
         record['genetical_risk'], record['insurance_plan'], record['employment_status'],
         record['gender'], record['marital_status'], record['bmi_category'],
         record['smoking_status'], record['region'], record['medical_history'])
        for record in transformed_data
    ]

    cursor.executemany(sql, batch_values)
    connection.commit()
    cursor.close()
    connection.close()

# Define the Tasks in the DAG
extract_task = PythonOperator(
    task_id='extract_data_from_supabase',
    python_callable=extract_data_from_supabase,
    dag=dag,
)

transform_task = PythonOperator(
    task_id='transform_data',
    python_callable=transform_data,
    op_args=[extract_task.output],  # Pass the extracted data to the transform function
    dag=dag,
)

load_task = PythonOperator(
    task_id='load_data_to_postgres',
    python_callable=load_data_to_postgres,
    op_args=[transform_task.output],  # Pass the transformed data to the load function
    dag=dag,
)

# Set Task Dependencies
extract_task >> transform_task >> load_task
