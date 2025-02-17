# database.py
from supabase import create_client, Client


# Set up the connection to Supabase (use your own URL and Key)
url = "https://vndclryqjcrarvhtpfrf.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZuZGNscnlxamNyYXJ2aHRwZnJmIiwicm9sZSI6ImFub24iLCJpYXQiOjE3Mzk3NDgwMDUsImV4cCI6MjA1NTMyNDAwNX0.LWu2AU3iJHZNCyHBw_1j-nh4yZBLop7PKShrr599OqU"
supabase: Client = create_client(url, key)

# Function to save user data to Supabase
def save_user_data_to_supabase(age, number_of_dependants, income_lakhs, genetical_risk, insurance_plan, 
                                employment_status, gender, marital_status, bmi_category, smoking_status, 
                                region, medical_history):
    data = {
        "age": age,
        "number_of_dependants": number_of_dependants,
        "income_lakhs": income_lakhs,
        "genetical_risk": genetical_risk,
        "insurance_plan": insurance_plan,
        "employment_status": employment_status,
        "gender": gender,
        "marital_status": marital_status,
        "bmi_category": bmi_category,
        "smoking_status": smoking_status,
        "region": region,
        "medical_history": medical_history
    }
    
    response = supabase.table("users").insert(data).execute()

    if response.data:  # ✅ If data is inserted, response.data will not be None
        print("Data inserted successfully")
    else:
        print("Error inserting data:", response.error)
