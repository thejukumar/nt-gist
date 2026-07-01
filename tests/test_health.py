"""Smoke test: the app imports and /health responds."""

from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_health_ok():
    resp = client.get("/health")
    assert resp.status_code == 200
    body = resp.json()
    assert body["status"] == "ok"
    assert "keys_configured" in body


def test_demo_run_returns_15_prompts():
    resp = client.post("/api/demo/run", json={"session_id": "x", "scenario": "telecom_support"})
    assert resp.status_code == 200
    assert len(resp.json()["prompts"]) == 15
