import os
from airflow import DAG
from airflow.providers.http.hooks.http import HttpHook
from airflow.providers.postgres.hooks.postgres import PostgresHook
import pendulum
from airflow.decorators import task
from airflow.utils.log.logging_mixin import LoggingMixin
from dotenv import load_dotenv

# Define Airflow Connection IDs
API_CONN_ID = 'supabase_api_conn'
POSTGRES_CONN_ID = 'pgadmin4_conn'

# Get Supabase Client API Key from environment variables
SUPABASE_CLIENT_API_KEY = os.getenv("SUPABASE_CLIENT_API_KEY")

# Define the DAG
with DAG(
    'realtime_etl_with_table_creation',
    description='Extract from Supabase, Transform (id - 2), and Load into PostgreSQL',
    schedule_interval='@hourly',
    start_date=pendulum.today('UTC').subtract(days=1),
    catchup=False
) as dag:
    
    @task()
    def extract_data_from_supabase():
        """Extract data from Supabase API using HttpHook."""
        http_hook = HttpHook(http_conn_id=API_CONN_ID, method='GET')
        endpoint = "/rest/v1/users?select=*"  # Only include the path, not the full URL

        headers = {
            'apikey': SUPABASE_CLIENT_API_KEY,
            'Authorization': f'Bearer {SUPABASE_CLIENT_API_KEY}',
            'Content-Type': 'application/json'
        }

        response = http_hook.run(endpoint, headers=headers)

        if response.status_code == 200:
            extracted_data = response.json()
            if not extracted_data:
                raise ValueError("No data extracted from Supabase")
            LoggingMixin().log.info(f"Extracted {len(extracted_data)} records from Supabase")
            return extracted_data
        else:
            raise ValueError(f"Error fetching data: {response.status_code} - {response.text}")
    
    @task()
    def transform_data(extracted_data):
        """Transform the extracted data."""
        if not extracted_data:
            raise ValueError("No data found in extracted_data")

        # Fetch local time
        local_time = pendulum.now("America/Toronto").to_datetime_string()

        transformed_data = []
        for record in extracted_data:
            transformed_data.append({
                "id": record.get("id", 0) - 2,
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
                "created_at": local_time  # Storing local PC time
            })
        
        LoggingMixin().log.info(f"Transformed {len(transformed_data)} records")
        return transformed_data
    
    @task()
    def load_data_to_postgres(transformed_data):
        """Create table if not exists and load data into PostgreSQL."""
        pg_hook = PostgresHook(postgres_conn_id=POSTGRES_CONN_ID)
        conn = pg_hook.get_conn()
        cursor = conn.cursor()
        
        # Create table if it doesn't exist
        cursor.execute(""" 
            CREATE TABLE IF NOT EXISTS users (
                id INT PRIMARY KEY,
                age INT,
                number_of_dependants INT,
                income_lakhs FLOAT,
                genetical_risk VARCHAR(50),
                insurance_plan VARCHAR(50),
                employment_status VARCHAR(50),
                gender VARCHAR(10),
                marital_status VARCHAR(50),
                bmi_category VARCHAR(50),
                smoking_status VARCHAR(50),
                region VARCHAR(50),
                medical_history TEXT,
                created_at TIMESTAMP
            );
        """)
        
        # Insert data
        sql = """
            INSERT INTO users (id, age, number_of_dependants, income_lakhs, genetical_risk, 
                              insurance_plan, employment_status, gender, marital_status, 
                              bmi_category, smoking_status, region, medical_history, created_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (id) DO NOTHING;
        """
        
        batch_values = [
            (record['id'], record['age'], record['number_of_dependants'], record['income_lakhs'],
             record['genetical_risk'], record['insurance_plan'], record['employment_status'],
             record['gender'], record['marital_status'], record['bmi_category'],
             record['smoking_status'], record['region'], record['medical_history'], record['created_at'])
            for record in transformed_data
        ]
        
        cursor.executemany(sql, batch_values)
        conn.commit()
        cursor.close()
        conn.close()
        
        LoggingMixin().log.info(f"Loaded {len(transformed_data)} records into PostgreSQL")
    
    # Set Task Dependencies
    extracted_data = extract_data_from_supabase()
    transformed_data = transform_data(extracted_data)
    load_data_to_postgres(transformed_data)
