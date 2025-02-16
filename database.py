import sqlite3
import pandas as pd

# Connect to the database (or create it)
conn = sqlite3.connect("user_data.db")
df = pd.read_sql_query("SELECT * FROM users", conn)
cursor = conn.cursor()

# Create table if it doesn't exist
cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        age INTEGER,
        number_of_dependants INTEGER,
        income_lakhs INTEGER,
        genetical_risk INTEGER,
        insurance_plan TEXT,
        employment_status TEXT,
        gender TEXT,
        marital_status TEXT,
        bmi_category TEXT,
        smoking_status TEXT,
        region TEXT,
        medical_history TEXT
    )
""")

conn.commit()
conn.close()

users_data = print(df)
