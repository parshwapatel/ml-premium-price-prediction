from flask import Flask, jsonify
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from datetime import datetime

app = Flask(__name__)

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
    return transformed_data

# Flask route to fetch real-time data
@app.route('/api/data', methods=['GET'])
def get_data():
    records = extract_data_from_supabase()
    transformed_data = transform_data(records)
    return jsonify(transformed_data)

# Flask app runner (This should be run independently)
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
