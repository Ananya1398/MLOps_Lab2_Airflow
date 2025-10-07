# Health Data ML Pipeline (Airflow)

## Overview
This project demonstrates how to use **Apache Airflow** to orchestrate a simple **machine learning workflow** for health data.  
The pipeline automatically reads, cleans, trains, and evaluates a machine learning model using scheduled Airflow DAGs.

---

## Prerequisites
- Python 3.11+
- pip
- virtualenv

---

## Steps to Run

### 1. Create and Activate Virtual Environment
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Initialize Airflow
```bash
airflow db init
```

### 4. Start Airflow in Standalone Mode
```bash
airflow standalone
```
This launches:
- Webserver (port 8080)  
- Scheduler  
- Triggerer  
- DAG Processor  

A login password for the `admin` user will be shown in the terminal or in  
`~/airflow/standalone_admin_password.txt`.

---

### 5. Access the Airflow UI
Open your browser and go to:

[http://localhost:8080](http://localhost:8080)

Login using the admin credentials displayed in your terminal.

---

### 6. Run the DAG
1. In the Airflow UI, unpause the DAG named **`health_data_training_dag`**.  
2. Click **Trigger DAG** to start execution.  
3. Monitor task logs in the UI to see outputs from:
   - Data cleaning  
   - Model training  
   - Model evaluation  

---

### 7. Outputs
- **Cleaned Dataset:** `clean_health_data.csv`  
- **Trained Model:** `model.pkl`  
- Model accuracy is logged in the Airflow task output.

