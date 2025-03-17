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

  bash 
  # Clone repository
  git clone https://github.com/parshwapatel/ml-premium-price-prediction.git
  cd ml-premium-price-prediction


2. Set Up Environment:-
   
    python -m venv venv
    source venv/bin/activate  # Windows: venv\Scripts\activate
    pip install -r requirements.txt


3. Configure Supabase:-

   Create a `.env` file in your project root:
   env:
     SUPABASE_URL='your-project-url.supabase.co'
     SUPABASE_KEY='your-anon-key-here'

   Database Schema (Supabase `users` Table)
   
      | Column Name            | Type        | Description & Example Values                     |
      |------------------------|-------------|--------------------------------------------------|
      | id                     | SERIAL      | Auto-incrementing unique identifier              |
      | age                    | INTEGER     | Age of the user (18-100)                         |
      | number_of_dependants   | INTEGER     | Number of dependents (0-20)                      |
      | income_lakhs           | NUMERIC     | Annual income in lakhs (e.g., 5 = ₹500,000)      |
      | genetical_risk         | INTEGER     | Genetic risk score (0-5 scale)                   |
      | insurance_plan         | VARCHAR     | Plan type: Bronze/Silver/Gold                    |
      | employment_status      | VARCHAR     | Employment type: Salaried/Self-Employed/Freelancer |
      | gender                 | VARCHAR     | Gender: Male/Female                              |
      | marital_status         | VARCHAR     | Marital status: Married/Unmarried                |
      | bmi_category           | VARCHAR     | BMI classification: Underweight/Normal/Overweight/Obesity |
      | smoking_status         | VARCHAR     | Smoking habits: Non-Smoker/Occasional/Regular    |
      | region                 | VARCHAR     | Geographic region: Northwest/Southeast/Northeast/Southwest |
      | medical_history        | VARCHAR     | Medical conditions: Diabetes/High BP/Heart Disease/etc. |
      | created_at             | TIMESTAMPTZ | Timestamp of record creation                     |


4. Build a services in docker-compose.yaml file:-


5. Launch Services:-
   
   -> Streamlit Web Application
      bash:
        streamlit run app/main.py
      Access: http://localhost:8501
    
   -> ## 🌪️ Airflow Setup with Astronomer

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
```  # <-- Closing backticks here

## PostgreSQL Database Setup

### Launch PostgreSQL Container
```bash
docker run --name project_hi \
  -e POSTGRES_PASSWORD=postgres \
  -p 5432:5432 \
  -d postgres:13
```  # <-- Closing backticks here
