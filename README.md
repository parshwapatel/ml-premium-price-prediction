1. Project Overview:-

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
  - Result visualization
- » Power BI Dashboards:
  - Demographic distribution
  - Premium cost analysis
  - Risk factor correlations
- » pgAdmin4 Database Management

##  Key Highlights
- 98% Model Accuracy (R-squared score)
- Real-Time Processing (<500ms prediction time)
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


## 2. Set Up Environment 

```bash
# Create virtual environment
python -m venv venv

# Activate environment
source venv/bin/activate  # Linux/macOS

# Install dependencies
pip install -r requirements.txt
```

## 3. Configure Supabase

### Environment Setup
Create `.env` file in project root:
```env
SUPABASE_URL='your-project-url.supabase.co'
SUPABASE_KEY='your-anon-key-here
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
 ## 4. Build a services in docker-compose.yaml file:-
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


   
  ## 5. Launch Services

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
