from flask import Flask, request, jsonify
import joblib
import pandas as pd
import os


# Create Flask application
app = Flask(__name__)


# Load trained flight price prediction model
MODEL_PATH = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "models",
    "flight_price_model.pkl"
)

model = joblib.load(MODEL_PATH)


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "status": "success",
        "message": "Travel Flight Price Prediction API is running"
    })


@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "healthy",
        "model_loaded": True
    })


@app.route("/predict", methods=["POST"])
def predict():

    try:
        data = request.get_json()

        required_features = [
            "from",
            "to",
            "flightType",
            "time",
            "distance",
            "agency",
            "year",
            "month",
            "day",
            "day_of_week"
        ]

        # Check whether all required inputs are provided
        missing_features = [
            feature for feature in required_features
            if feature not in data
        ]

        if missing_features:
            return jsonify({
                "status": "error",
                "message": "Missing required features",
                "missing_features": missing_features
            }), 400

        # Convert input into DataFrame
        input_data = pd.DataFrame([data])[required_features]

        # Make prediction
        prediction = model.predict(input_data)[0]

        return jsonify({
            "status": "success",
            "predicted_price": round(float(prediction), 2)
        })

    except Exception as e:

        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )