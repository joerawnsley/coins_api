from src.app import app
from fastapi.testclient import TestClient
import os, logging

if os.getenv('DB_LOGGING') == 'on':
    logging.getLogger('peewee').addHandler(logging.StreamHandler())
    logging.getLogger('peewee').setLevel(logging.DEBUG)

# ------------ create test client ----------------
client = TestClient(app)

# ----- welcome endpoint -----

def test_home_route_returns_message():
    response = client.get("/")
    assert response.status_code == 200
    assert "Welcome" in response.text

def test_home_route_returns_json_object():
    response = client.get("/")
    data = response.json()
    assert isinstance(data, dict)