from datetime import datetime

from airflow import DAG
from airflow.operators.python import PythonOperator


MODEL_PATH = "/opt/airflow/models/flight_price_model.pkl"


def validate_model():
    import joblib

    model = joblib.load(MODEL_PATH)

    print("Model loaded successfully.")
    print("Model type:", type(model).__name__)


def evaluate_model():
    import joblib
    import numpy as np

    model = joblib.load(MODEL_PATH)

    sample = {
        "from": ["Recife (PE)"],
        "to": ["Florianopolis (SC)"],
        "flightType": ["firstClass"],
        "time": [1.76],
        "distance": [676.53],
        "agency": ["FlyingDrops"],
        "year": [2025],
        "month": [1],
        "day": [15],
        "day_of_week": [3],
    }

    import pandas as pd

    X = pd.DataFrame(sample)

    prediction = model.predict(X)

    print("Sample prediction:", float(np.asarray(prediction)[0]))


with DAG(
    dag_id="travel_price_pipeline",
    start_date=datetime(2026, 8, 25),
    schedule=None,
    catchup=False,
    tags=["travel", "ml", "mlops"],
) as dag:

    validate_task = PythonOperator(
        task_id="validate_model",
        python_callable=validate_model,
    )

    evaluate_task = PythonOperator(
        task_id="evaluate_model",
        python_callable=evaluate_model,
    )

    validate_task >> evaluate_task
