# Health Insurance Premium Prediction System

An end-to-end machine learning system that predicts health insurance premiums with **98% accuracy** using XGBoost, featuring real-time data pipelines and interactive analytics.

##  Key Features

###  Machine Learning Model
- » XGBoost with RandomizedCV hyperparameter tuning
- » Processes 12+ health parameters:
  - Age, BMI, Medical History
  - Lifestyle Factors (Smoking Status, Genetic Risk)
  - Demographic Data (Income, Region)
- » Automated feature scaling with StandardScaler

###  Real-Time Data Flow
- » Supabase PostgreSQL integration (`users` table)
- » Airflow ETL Pipelines (Docker containers)
- » Automated data validation rules:
  - Age range: 18-100
  - Income validation: 0-200 lakhs
  - BMI category mapping

###  Interactive Analytics
- » Streamlit Web Interface:
  - Real-time premium predictions
  - User input validation
- » Power BI Dashboards:
  - Demographic distribution
  - Premium cost analysis
  - Risk factor correlations
- » pgAdmin4 Database Management
  - Storing user inputs into database

##  Key Highlights
- 98% Model Accuracy 
- Real-Time Processing 
- Scalable Architecture (Docker containers)
- Secure Data Handling (Supabase RLS enabled)
  
  
## Tech Stack 

| Component           | Technologies Used                          |
|---------------------|--------------------------------------------|
| Machine Learning | Python, Scikit-learn, XGBoost, Pandas      |
| Frontend      | Streamlit                                  |
| Database      | Supabase (PostgreSQL), pgAdmin4            |
| Data Engineering | Apache Airflow, Docker, REST API           |
| DevOps         | Docker Desktop, Postman                    |
  
  
## Installation 

### Prerequisites
-  Python 3.8+ - Required for running the ML model and Streamlit app  
  [Download Python](https://www.python.org/downloads/)
  
-  Docker Desktop - For containerized services (PostgreSQL and Airflow)  
  [Install Docker](https://www.docker.com/products/docker-desktop)

-  Postman - For API testing and development  
  [Get Postman](https://www.postman.com/downloads/)

-  pgAdmin4 - PostgreSQL database management GUI  
  [Install pgAdmin](https://www.pgadmin.org/download/)

### Verify Installations
```bash
# Check Python version
python --version

# Check Docker installation
docker --version

# Check Docker Compose version
docker-compose --version
## 1. Clone Repository 

```bash
# Clone the repository
git clone https://github.com/parshwapatel/ml-premium-price-prediction.git

# Navigate to project directory
cd ml-premium-price-prediction
```


##  Set Up Environment 

```bash
# Create virtual environment
python -m venv venv

# Activate environment
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate  #Windows

# Install dependencies
pip install -r requirements.txt
```

##  Configure Supabase

### Environment Setup
Create `.env` file in project root:
```env
SUPABASE_URL='your-project-url.supabase.co'
SUPABASE_CLIENT_API_KEY='your-anon-key-here
```
Database Schema (users Table)
| Column                | Type           | Description & Example Values                              |
|-----------------------|----------------|-----------------------------------------------------------|
| `id`                  | SERIAL         | Auto-generated unique ID                                  |
| `age`                 | INTEGER        | User age (18-100)                                         |
| `number_of_dependants`| INTEGER        | Dependents count (0-20)                                   |
| `income_lakhs`        | NUMERIC        | Annual income (e.g., 5 = ₹500,000)                        |
| `genetical_risk`      | INTEGER        | Genetic risk score (0-5 scale)                            |
| `insurance_plan`      | VARCHAR(50)    | Plan type: Bronze/Silver/Gold                             |
| `employment_status`   | VARCHAR(50)    | Salaried/Self-Employed/Freelancer                         |
| `gender`              | VARCHAR(10)    | Male/Female                                               |
| `marital_status`      | VARCHAR(20)    | Married/Unmarried                                         |
| `bmi_category`        | VARCHAR(20)    | Underweight/Normal/Overweight/Obesity                     |
| `smoking_status`      | VARCHAR(20)    | Non-Smoker/Occasional/Regular                             |
| `region`              | VARCHAR(20)    | Northwest/Southeast/Northeast/Southwest                   |
| `medical_history`     | VARCHAR(100)   | Diabetes/High BP/Heart Disease/etc.                       |
| `created_at`          | TIMESTAMPTZ    | Auto-generated timestamp (with timezone)                  |
 ##  Build a services in docker-compose.yaml file:-
 ```code
version: '3'
services:
  postgres:
    image: postgres:13
    container_name: postgres_db
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: postgres
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  airflow:
    environment:
      - SUPABASE_CLIENT_API_KEY=${SUPABASE_CLIENT_API_KEY}
    env_file:
      - .env

volumes:
  postgres_data:
```


   
  ##  Launch Services

###  Streamlit Web Application
```bash
streamlit run app/main.py
```

### Launch Airflow Services
```bash
# Switch to Airflow branch
git checkout astro-airflow-run

# Install Astronomer CLI
npm install -g astro

# Initialize project
astro dev init

# Start services
astro dev start 
```  

## PostgreSQL Database Setup

### Launch PostgreSQL Container
```bash
docker run --name project_hi \
  -e POSTGRES_PASSWORD=postgres \
  -p 5432:5432 \
  -d postgres:13
```

## Airflow Connections Setup

This project uses the following Airflow connections. Ensure these are configured in your Airflow environment:

### 1. Supabase API Connection
- **Connection ID**: `supabase_api_conn`
- **Type**: HTTP
- **Required Parameters**:
  - Host: Your Supabase project URL (e.g., `https://<project-id>.supabase.co`)
  - Authentication: Add API key to `Password` field (or use `Extras` for custom headers)

### 2. PostgreSQL Database Connection
- **Connection ID**: `pgadmin4_conn`
- **Type**: Postgres
- **Required Parameters**:
  - Host: Database server address
  - Schema: Database name
  - Login: Database username
  - Password: Database password
  - Port: 5432 (default) or your custom port

## Airflow Connections Configuration

### 1. PostgreSQL Database Connection (pgadmin4_conn)
**Connection Details**:
```bash
Connection ID: pgadmin4_conn
Connection Type: Postgres
Host: Container_ID
Database: postgres
Login: postgres
Password: postgres
Port: 5432
```

### 2. Supabase API Connection (supabase_api_conn)
```bash
Connection ID: supabase_api_conn
Connection Type: HTTP
Host: your-project-url.supabase.co
Extras JSON:
{
  "apikey": "your-supabase-api-key",
  "Authorization": "Bearer your-supabase-bearer-token"
}
```

## Workflow Dependencies

The data pipeline follows this execution order:

```python
# Set Task Dependencies
extracted_data = extract_data_from_supabase()
transformed_data = transform_data(extracted_data)
load_data_to_postgres(transformed_data)

# Define execution sequence
extracted_data >> transformed_data >> load_data_to_postgres
```


## Health Insurance Web Visitors Dashboard (Power BI)

## Project Overview
This Power BI dashboard visualizes data from a PostgreSQL database containing health insurance web visitor information, including demographics, income, insurance plans, and medical history. The dashboard is built using **DirectQuery** for real-time data updates.

## Prerequisites
1. Power BI Desktop ([Download here](https://powerbi.microsoft.com/desktop/))
2. PostgreSQL ODBC Driver ([Download here](https://www.postgresql.org/ftp/odbc/versions/))
3. Access to the PostgreSQL database with the following credentials:
   - Hostname/IP: localhost
   - Port (default: 5432)
   - Database name : postgres
   - Username and password : postgres

## Steps to Replicate the Project

### 1. Connect Power BI to PostgreSQL
1. Open Power BI Desktop.
2. ClickGet Data > Database > PostgreSQL.
3. Enter your PostgreSQL connection details:
   - Server: localhost
   - Database: postgres
4. Select `DirectQuery` for live data connectivity.
5. Load the `users` table.

### 2. Create Age Group Distribution (Bar Chart)
1. Create a new column using this DAX formula:
   ```dax
   Age Group = 
   SWITCH(
       TRUE(),
       'users'[age] >= 0 && 'users'[age] <= 25, "0-25",
       'users'[age] > 25 && 'users'[age] <= 50, "25-50",
       'users'[age] > 50 && 'users'[age] <= 75, "50-75",
       'users'[age] > 75 && 'users'[age] <= 100, "75-100",
       "Other"
   )
Drag Age Group to the X-axis and id (count) to the Y-axis.

Customize the bar chart using the Format pane.

### 3. Create Income Group Distribution (Pie Chart)
Create a new column using this DAX formula:

```dax
Income Group = 
SWITCH(
    TRUE(),
    'users'[income_lakhs] >= 0 && 'users'[income_lakhs] < 20, "0-20",
    'users'[income_lakhs] >= 20 && 'users'[income_lakhs] < 50, "20-50",
    'users'[income_lakhs] >= 50 && 'users'[income_lakhs] < 75, "50-75",
    'users'[income_lakhs] >= 75 && 'users'[income_lakhs] < 100, "75-100",
    "100+"
)
```
Use Income Group in the Legend and id (count) in Values.

Fix legend order by creating a sort-order column (see Troubleshooting).

### 4. Insurance Plan Metrics (Cards)
Create DAX measures for each plan:

```dax
% Bronze Plan = 
DIVIDE(
    COUNTROWS(FILTER('users', 'users'[insurance_plan] = "Bronze")),
    COUNTROWS('users'),
    0
)
```
Repeat for Silver and Gold plans.

Add these measures to Card visuals.

### 5. Medical History Analysis
Use a Word Cloud or Bar Chart:

Drag medical_history to the Category field.

Drag id to Values for counts.

##### (For questions or feedback, contact me at parshwa1131@gmail.com) #####

