import joblib
import mlflow

MODEL_PATH = "models/flight_price_model.pkl"

# MLflow SQLite tracking backend
mlflow.set_tracking_uri("sqlite:///mlflow.db")

# Create or use experiment
mlflow.set_experiment("Travel Flight Price Prediction")

# Verify existing model can be loaded
model = joblib.load(MODEL_PATH)

# Best parameters from existing RandomizedSearchCV run
best_params = {
    "n_estimators": 50,
    "max_depth": 20,
    "min_samples_split": 5,
    "min_samples_leaf": 1,
    "max_features": "log2"
}

# Existing model evaluation metrics
metrics = {
    "MAE": 0.0165,
    "RMSE": 0.1329,
    "R2": 1.0
}

with mlflow.start_run(run_name="RandomForest_Tuned"):

    # Log hyperparameters
    mlflow.log_params(best_params)

    # Log metrics
    mlflow.log_metrics(metrics)

    # Log metadata
    mlflow.set_tag(
        "model_type",
        "RandomForestRegressor"
    )

    mlflow.set_tag(
        "features",
        "from,to,flightType,time,distance,agency"
    )

    mlflow.set_tag(
        "source",
        "Existing trained notebook model"
    )

    mlflow.set_tag(
        "artifact_type",
        "joblib_pickle"
    )

    # Log the existing .pkl file directly
    mlflow.log_artifact(
        MODEL_PATH,
        artifact_path="model"
    )

    print("MLflow run completed successfully.")
    print(
        "Run ID:",
        mlflow.active_run().info.run_id
    )