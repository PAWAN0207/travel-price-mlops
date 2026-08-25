import requests

BASE_URL = "http://127.0.0.1:5000"


def test_home():
    response = requests.get(f"{BASE_URL}/", timeout=10)

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "success"


def test_health():
    response = requests.get(f"{BASE_URL}/health", timeout=10)

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "healthy"
    assert data["model_loaded"] is True


def test_predict():
    payload = {
        "from": "Recife (PE)",
        "to": "Florianopolis (SC)",
        "flightType": "firstClass",
        "time": 1.76,
        "distance": 676.53,
        "agency": "FlyingDrops"
    }

    response = requests.post(
        f"{BASE_URL}/predict",
        json=payload,
        timeout=30
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "success"
    assert "predicted_price" in data
    assert isinstance(data["predicted_price"], (int, float))
    assert data["predicted_price"] > 0
