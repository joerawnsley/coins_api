from app import app
from fastapi.testclient import TestClient

client = TestClient(app)

def test_root_returns_message():
    response = client.get("/")
    assert response.status_code == 200
    assert "Welcome" in response.text

def test_root_returns_json_object():
    response = client.get("/")
    data = response.json()
    assert isinstance(data, dict)

def test_coins_route_returns_a_list():
    response = client.get("/coins")
    data = response.json()
    assert isinstance(data, list)