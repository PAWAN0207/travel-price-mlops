from datetime import datetime

import mlflow
import mlflow.sklearn
from airflow import DAG
from airflow.operators.python import PythonOperator


MODEL_PATH = "/opt/airflow/models/flight_price_model.pkl"

# IMPORTANT:
# Airflow container se MLflow container ko access karne ke liye
# localhost nahi, Docker service name use karna hai.
MLFLOW_TRACKING_URI = "http://mlflow:5000"

EXPERIMENT_NAME = "travel-price-prediction"


def validate_model():
    import joblib

    model = joblib.load(MODEL_PATH)

    print("========================================")
    print("MODEL VALIDATION")
    print("========================================")
    print("Model loaded successfully.")
    print("Model type:", type(model).__name__)
    print("Model path:", MODEL_PATH)
    print("========================================")


def evaluate_model():

    import joblib
    import numpy as np
    import pandas as pd

    # Connect Airflow → MLflow
    mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)

    # Create experiment if it doesn't already exist
    mlflow.set_experiment(EXPERIMENT_NAME)

    # Load model
    model = joblib.load(MODEL_PATH)

    # Sample input
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

    X = pd.DataFrame(sample)

    # Start MLflow run
    with mlflow.start_run(run_name="flight-price-evaluation"):

        # Model information
        mlflow.log_param(
            "model_type",
            type(model).__name__
        )

        mlflow.log_param(
            "flight_type",
            sample["flightType"][0]
        )

        mlflow.log_param(
            "agency",
            sample["agency"][0]
        )

        mlflow.log_param(
            "from",
            sample["from"][0]
        )

        mlflow.log_param(
            "to",
            sample["to"][0]
        )

        # Numerical parameters
        mlflow.log_param(
            "time",
            sample["time"][0]
        )

        mlflow.log_param(
            "distance",
            sample["distance"][0]
        )

        mlflow.log_param(
            "year",
            sample["year"][0]
        )

        mlflow.log_param(
            "month",
            sample["month"][0]
        )

        mlflow.log_param(
            "day",
            sample["day"][0]
        )

        mlflow.log_param(
            "day_of_week",
            sample["day_of_week"][0]
        )

        # Prediction
        prediction = model.predict(X)

        predicted_price = float(
            np.asarray(prediction)[0]
        )

        # Log prediction as metric
        mlflow.log_metric(
            "predicted_price",
            predicted_price
        )

        # Log model file as artifact
        mlflow.log_artifact(
            MODEL_PATH,
            artifact_path="model"
        )

        print("========================================")
        print("MLFLOW RUN COMPLETED")
        print("========================================")
        print("Experiment:", EXPERIMENT_NAME)
        print("Tracking URI:", MLFLOW_TRACKING_URI)
        print("Run ID:", mlflow.active_run().info.run_id)
        print("Predicted price:", predicted_price)
        print("========================================")


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