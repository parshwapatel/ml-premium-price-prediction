import streamlit as st
from prediction_helper import predict
import base64
import sqlite3


def set_background(image_file):
    with open(image_file, "rb") as img:
        encoded_string = base64.b64encode(img.read()).decode()

    st.markdown(
        f"""
        <style>
        .stApp {{
            background: linear-gradient(rgba(0, 0, 0, 0.8), rgba(0, 0, 0, 0.8)), 
                        url("data:image/jpg;base64,{encoded_string}") no-repeat center center fixed;
            background-size: cover;
            padding-bottom: 100px; /* To ensure footer doesn't overlap content */
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Call the function after setting the title
st.title('Health Insurance Cost Predictor')
st.markdown("<br><br>", unsafe_allow_html=True)  # Extra space after title
set_background("pic_hi.jpg")  # Ensure the image is in the same folder

categorical_options = {
    'Gender': ['Male', 'Female'],
    'Marital Status': ['Unmarried', 'Married'],
    'BMI Category': ['Normal', 'Obesity', 'Overweight', 'Underweight'],
    'Smoking Status': ['No Smoking', 'Regular', 'Occasional'],
    'Employment Status': ['Salaried', 'Self-Employed', 'Freelancer', ''],
    'Region': ['Northwest', 'Southeast', 'Northeast', 'Southwest'],
    'Medical History': [
        'No Disease', 'Diabetes', 'High blood pressure', 'Diabetes & High blood pressure',
        'Thyroid', 'Heart disease', 'High blood pressure & Heart disease', 'Diabetes & Thyroid',
        'Diabetes & Heart disease'
    ],
    'Insurance Plan': ['Bronze', 'Silver', 'Gold']
}

# Create four rows of three columns each
row1 = st.columns(3)
row2 = st.columns(3)
row3 = st.columns(3)
row4 = st.columns(3)

# Assign inputs to the grid
with row1[0]:
    age = st.number_input('Age', min_value=18, step=1, max_value=100)
with row1[1]:
    number_of_dependants = st.number_input('Number of Dependants', min_value=0, step=1, max_value=20)
with row1[2]:
    income_lakhs = st.number_input('Income in Lakhs', step=1, min_value=0, max_value=200)

with row2[0]:
    genetical_risk = st.selectbox('Genetical Risk', [0, 1, 2, 3, 4, 5])
with row2[1]:
    insurance_plan = st.selectbox('Insurance Plan', categorical_options['Insurance Plan'])
with row2[2]:
    employment_status = st.selectbox('Employment Status', categorical_options['Employment Status'])

with row3[0]:
    gender = st.selectbox('Gender', categorical_options['Gender'])
with row3[1]:
    marital_status = st.selectbox('Marital Status', categorical_options['Marital Status'])
with row3[2]:
    bmi_category = st.selectbox('BMI Category', categorical_options['BMI Category'])

with row4[0]:
    smoking_status = st.selectbox('Smoking Status', categorical_options['Smoking Status'])
with row4[1]:
    region = st.selectbox('Region', categorical_options['Region'])
with row4[2]:
    medical_history = st.selectbox('Medical History', categorical_options['Medical History'])

# Create a dictionary for input values
input_dict = {
    'Age': age,
    'Number of Dependants': number_of_dependants,
    'Income in Lakhs': income_lakhs,
    'Genetical Risk': genetical_risk,
    'Insurance Plan': insurance_plan,
    'Employment Status': employment_status,
    'Gender': gender,
    'Marital Status': marital_status,
    'BMI Category': bmi_category,
    'Smoking Status': smoking_status,
    'Region': region,
    'Medical History': medical_history
}

# Custom styling for the button and success message
st.markdown("""
    <style>
        .stButton>button {
            background-color: #007bff; /* Blue color */
            color: white; /* White text */
            font-size: 16px; /* Larger text */
            padding: 15px 32px; /* Increased padding for bigger button */
            border-radius: 5px; /* Rounded corners */
            border: none; /* Remove default border */
            cursor: pointer; /* Pointer cursor on hover */
            transition: background-color 0.3s ease;
        }
        .stButton>button:hover {
            background-color: #0056b3; /* Darker blue on hover */
        }
    </style>
    """, unsafe_allow_html=True)


st.markdown("""
    <style>
        .success-message {
            background-color: #28a745; /* Green background */
            color: white; /* White text */
            padding: 15px; /* Padding around text */
            border-radius: 5px; /* Rounded corners */
            font-size: 18px; /* Larger text */
            font-weight: bold; /* Make text bold */
            text-align: center; /* Center align the text */
        }
    </style>
    """, unsafe_allow_html=True)

# adding data to the database

def save_user_data(age, number_of_dependants, income_lakhs, genetical_risk, 
                   insurance_plan, employment_status, gender, marital_status, 
                   bmi_category, smoking_status, region, medical_history):
    conn = sqlite3.connect("user_data.db")
    cursor = conn.cursor()

    # creating table
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
        medical_history TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
""")
    
    cursor.execute("""
        INSERT INTO users (age, number_of_dependants, income_lakhs, genetical_risk, 
                           insurance_plan, employment_status, gender, marital_status, 
                           bmi_category, smoking_status, region, medical_history) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (age, number_of_dependants, income_lakhs, genetical_risk, insurance_plan, 
          employment_status, gender, marital_status, bmi_category, smoking_status, 
          region, medical_history))
    conn.commit()
    conn.close()

# Display the prediction result with the custom styling
if st.button('Predict'):
    prediction = predict(input_dict)
    save_user_data(age, number_of_dependants, income_lakhs, genetical_risk, 
                   insurance_plan, employment_status, gender, marital_status, 
                   bmi_category, smoking_status, region, medical_history)
    st.markdown(f'<div class="success-message">Your Predicted Health Insurance Cost: {prediction}</div>', unsafe_allow_html=True)

# Add footer that appears after scrolling
st.markdown("""
    <style>
        .footer {
            width: 100%;
            text-align: center;
            padding: 10px;
            background-color: rgba(0, 0, 0, 0.6); /* Slightly transparent black background */
            font-size: 12px; /* Small text size */
            color: white; /* White text */
            position: fixed;
            bottom: 0;
            left: 0;
            z-index: 9999;
        }
    </style>
    <div class="footer">
        &copy; 2025 All Rights Reserved | Parshwa P.
    </div>
    """, unsafe_allow_html=True)
