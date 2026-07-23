from fastapi.testclient import TestClient

from src.main import app


def test_health_check() -> None:
    client = TestClient(app)
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_alert_ingest_and_remediation() -> None:
    client = TestClient(app)
    ingest_response = client.post(
        "/alerts",
        json={
            "alert_id": "alert-001",
            "severity": "high",
            "category": "latency",
            "message": "Prediction latency exceeded threshold.",
        },
    )
    assert ingest_response.status_code == 200
    assert ingest_response.json()["alert_id"] == "alert-001"

    remediation_response = client.post("/remediate", json={"alert_id": "alert-001"})
    assert remediation_response.status_code == 200
    payload = remediation_response.json()
    assert payload["recommendations"]
    assert "latency" in payload["summary"].lower()
