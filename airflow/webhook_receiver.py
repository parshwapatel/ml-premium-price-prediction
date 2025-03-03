from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

AIRFLOW_TRIGGER_URL = "http://localhost:8080/api/v1/dags/realtime_etl11/dagRuns"
AIRFLOW_USERNAME = "airflow"
AIRFLOW_PASSWORD = "airflow"

@app.route('/supabase-webhook', methods=['POST'])


def receive_supabase_data():
    data = request.json  # Incoming data from Supabase
    
    # Trigger Airflow DAG
    response = requests.post(
        AIRFLOW_TRIGGER_URL,
        json={"conf": data},  # Send data as DAG configuration
        auth=(AIRFLOW_USERNAME, AIRFLOW_PASSWORD)
    )
    
    return jsonify({"message": "Triggered Airflow DAG", "status": response.status_code})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)  # Run on Airflow machine
