from fastapi.testclient import TestClient

from app.main import app


def test_health():
    with TestClient(app) as client:
        resp = client.get("/health")
        assert resp.status_code == 200
        assert resp.json()["status"] == "ok"


def test_predict_positivo():
    with TestClient(app) as client:
        resp = client.post("/predict", json={"text": "me encanta es excelente y maravilloso"})
        assert resp.status_code == 200
        body = resp.json()
        assert body["label"] == "positivo"
        assert 0.0 <= body["confidence"] <= 1.0


def test_predict_negativo():
    with TestClient(app) as client:
        resp = client.post("/predict", json={"text": "horrible pesimo lo odio fue terrible"})
        assert resp.status_code == 200
        assert resp.json()["label"] == "negativo"


def test_predict_validacion():
    with TestClient(app) as client:
        resp = client.post("/predict", json={"text": ""})
        assert resp.status_code == 422  # texto vacío rechazado por pydantic


def test_metrics():
    with TestClient(app) as client:
        client.post("/predict", json={"text": "muy bueno"})
        resp = client.get("/metrics")
        assert resp.status_code == 200
        assert resp.json()["predictions_total"] >= 1
