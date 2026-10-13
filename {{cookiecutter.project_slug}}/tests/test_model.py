
from fastapi.testclient import TestClient
from app.main import app


def test_home():
    with TestClient(app) as client:
        response = client.get("/")
        assert response.status_code == 200


def test_health():
    with TestClient(app) as client:
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"


def test_prediction():
    with TestClient(app) as client:
        response = client.post(
            "/predict",
            json={
                "sepal_length": 5.1,
                "sepal_width": 3.5,
                "petal_length": 1.4,
                "petal_width": 0.2
            }
        )

        assert response.status_code == 200
        assert response.json()["prediction"] == 0
        assert response.json()["species"] == "setosa"
