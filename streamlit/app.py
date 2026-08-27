import os
import streamlit as st
import requests


# --------------------------------------------------
# Page Configuration
# --------------------------------------------------

st.set_page_config(
    page_title="Travel Price Predictor",
    page_icon="✈️",
    layout="centered"
)


# --------------------------------------------------
# API Configuration
# --------------------------------------------------

API_URL = os.getenv("API_URL", "http://localhost:5000")


# --------------------------------------------------
# Title
# --------------------------------------------------

st.title("✈️ Travel Flight Price Predictor")

st.write(
    "Enter your flight details below to estimate the ticket price."
)


# --------------------------------------------------
# Input Form
# --------------------------------------------------

with st.form("prediction_form"):

    col1, col2 = st.columns(2)

    with col1:

        from_city = st.text_input(
            "From",
            value="Recife (PE)"
        )

        flight_type = st.selectbox(
            "Flight Type",
            [
                "economy",
                "firstClass",
                "premiumEconomy",
                "business"
            ],
            index=1
        )

        time = st.number_input(
            "Flight Time",
            min_value=0.1,
            max_value=30.0,
            value=1.76,
            step=0.01
        )

        agency = st.text_input(
            "Agency",
            value="FlyingDrops"
        )

        year = st.number_input(
            "Year",
            min_value=2020,
            max_value=2035,
            value=2026,
            step=1
        )

    with col2:

        to_city = st.text_input(
            "To",
            value="Florianopolis (SC)"
        )

        distance = st.number_input(
            "Distance (km)",
            min_value=1.0,
            value=676.53,
            step=0.01
        )

        month = st.number_input(
            "Month",
            min_value=1,
            max_value=12,
            value=8,
            step=1
        )

        day = st.number_input(
            "Day",
            min_value=1,
            max_value=31,
            value=28,
            step=1
        )

        day_of_week = st.number_input(
            "Day of Week",
            min_value=0,
            max_value=6,
            value=5,
            step=1
        )

    submitted = st.form_submit_button(
        "Predict Flight Price"
    )


# --------------------------------------------------
# Prediction
# --------------------------------------------------

if submitted:

    payload = {
        "from": from_city,
        "to": to_city,
        "flightType": flight_type,
        "time": time,
        "distance": distance,
        "agency": agency,
        "year": year,
        "month": month,
        "day": day,
        "day_of_week": day_of_week
    }

    try:

        with st.spinner("Predicting flight price..."):

            response = requests.post(
                f"{API_URL}/predict",
                json=payload,
                timeout=10
            )

        if response.status_code == 200:

            result = response.json()

            predicted_price = result.get(
                "predicted_price"
            )

            if predicted_price is not None:

                st.success("Prediction successful!")

                st.metric(
                    "Predicted Flight Price",
                    f"₹ {predicted_price:,.2f}"
                )

            else:

                st.error(
                    "API returned a successful response, "
                    "but no predicted price was found."
                )

        else:

            try:

                result = response.json()

                st.error(
                    result.get(
                        "message",
                        "Prediction failed."
                    )
                )

            except Exception:

                st.error(
                    f"Prediction failed. "
                    f"API returned status {response.status_code}."
                )

    except requests.exceptions.ConnectionError:

        st.error(
            "Could not connect to the Flask API. "
            "Make sure the API is running on port 5000."
        )

    except requests.exceptions.Timeout:

        st.error(
            "The API request timed out."
        )

    except Exception as e:

        st.error(
            f"Unexpected error: {str(e)}"
        )


# --------------------------------------------------
# API Health Check
# --------------------------------------------------

st.divider()

if st.button("Check API Health"):

    try:

        response = requests.get(
            f"{API_URL}/health",
            timeout=5
        )

        if response.status_code == 200:

            health = response.json()

            st.success(
                f"API Status: {health['status']} | "
                f"Model Loaded: {health['model_loaded']}"
            )

        else:

            st.error(
                "API health check failed."
            )

    except requests.exceptions.ConnectionError:

        st.error(
            "API is not reachable. "
            "Make sure Flask API is running on port 5000."
        )

    except requests.exceptions.Timeout:

        st.error(
            "API health check timed out."
        )

    except Exception as e:

        st.error(
            f"Health check error: {str(e)}"
        )