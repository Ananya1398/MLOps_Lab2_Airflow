from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.operators.empty import EmptyOperator
from airflow.utils.trigger_rule import TriggerRule
from src.model_development import clean_data, train_model, evaluate_model

default_args = {
    'owner': 'ananya',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=2),
}

with DAG(
    dag_id='health_data_training_dag',
    default_args=default_args,
    description='Train & evaluate health risk classifier',
    schedule=None,
    start_date=datetime(2025, 10, 1),
    catchup=False,
    tags=['health', 'ml', 'lab2'],
) as dag:

    start = EmptyOperator(task_id='start')

    clean_task = PythonOperator(
        task_id='clean_data',
        python_callable=clean_data,
    )

    train_task = PythonOperator(
        task_id='train_model',
        python_callable=train_model,
    )

    eval_task = PythonOperator(
        task_id='evaluate_model',
        python_callable=evaluate_model,
    )

    def check_accuracy(**context):
        acc = context['ti'].xcom_pull(task_ids='evaluate_model')
        if acc >= 0.80:
            return 'end_success'
        return 'end_failure'

    branch_task = BranchPythonOperator(
        task_id='check_accuracy_branch',
        python_callable=check_accuracy,
    )

    # simple placeholder end tasks instead of emails
    end_success = EmptyOperator(task_id='end_success')
    end_failure = EmptyOperator(task_id='end_failure', trigger_rule=TriggerRule.ONE_FAILED)

    start >> clean_task >> train_task >> eval_task >> branch_task

