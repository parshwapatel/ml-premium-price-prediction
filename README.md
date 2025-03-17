1. Project Overview:-

  Health Insurance Premium Prediction System:-
  
  Predict health insurance costs with 98% accuracy using machine learning, powered by real-time data pipelines and interactive analytics.
  
  Live Application: [Streamlit Web App](https://get-health-insurance-price.streamlit.app/)
  
  
  Features:-
  - Machine Learning Model 
    » XGBoost with RandomizedCV hyperparameter tuning  
    » 98% prediction accuracy  
    » Processes age, BMI, medical history, and lifestyle factors
  
  - Real-Time Data Flow
    » User inputs stored in Supabase PostgreSQL (`users` table)  
    » Airflow ETL pipelines (Dockerized)  
    » Automated data validation and cleaning
  
  - Interactive Analytics
    » Streamlit web interface for instant predictions  
    » Power BI dashboards for demographic insights  
    » pgAdmin4 database management
  
  
  Tech Stack:-
  
  | Component              | Technologies Used                          |
  |------------------------|--------------------------------------------|
  | Machine Learning       | Python, Scikit-learn, XGBoost, Pandas      |
  | Frontend               | Streamlit                                  |
  | Database               | Supabase (PostgreSQL), pgAdmin4            |
  | Data Engineering       | Apache Airflow, Docker, REST API           |
  | DevOps                 | Docker Desktop, Postman                    |
  
  
  Installation:-
  
  Prerequisites:-
  - Python 3.8+
  - Docker Desktop
  - Postman (for API testing)
  - PgAdmin4

## 1. Clone Repository 📥

```bash
# Clone the repository
git clone https://github.com/parshwapatel/ml-premium-price-prediction.git

# Navigate to project directory
cd ml-premium-price-prediction
```


## 2. Set Up Environment ⚙️

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
