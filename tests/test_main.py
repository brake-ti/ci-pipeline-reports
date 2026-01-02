from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_health_live():
    response = client.get("/health/live")
    assert response.status_code == 200
    assert response.json() == {"status": "alive"}

def test_version():
    response = client.get("/version")
    assert response.status_code == 200
    assert "version" in response.json()
    assert "_links" in response.json()
