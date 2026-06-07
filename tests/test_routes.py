from app import app
from fastapi.testclient import TestClient

client = TestClient(app)

def test_root_returns_message():
    response = client.get("/")
    assert response.status_code == 200
    assert "Welcome" in response.text