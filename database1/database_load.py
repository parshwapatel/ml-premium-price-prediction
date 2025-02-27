#database_load.py

import psycopg2
from sqlalchemy import create_engine

def save_user_data_to_postgres(age, num_dependants, income, genetical_risk, insurance_plan, employment_status, gender, marital_status, bmi_category, smoking_status, region, medical_history):
    conn = psycopg2.connect("dbname=test user=postgres password=secret")
    cursor = conn.cursor()

    # Insert data into your table
    cursor.execute("""
        INSERT INTO user_data (age, num_dependants, income, genetical_risk, insurance_plan, employment_status, gender, marital_status, bmi_category, smoking_status, region, medical_history)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (age, num_dependants, income, genetical_risk, insurance_plan, employment_status, gender, marital_status, bmi_category, smoking_status, region, medical_history))

    conn.commit()
    cursor.close()
    conn.close()
