from app import app
from fastapi.testclient import TestClient
from src.database import db
import pytest, json
from src.models import Coin, Duty


client = TestClient(app)

# ----- basic routes -----

def test_root_returns_message():
    response = client.get("/")
    assert response.status_code == 200
    assert "Welcome" in response.text

def test_root_returns_json_object():
    response = client.get("/")
    data = response.json()
    assert isinstance(data, dict)

# ----- test with full database -----

with open('seed_data/seed_data.json') as json_data:
    seed_data = json.load(json_data)
    all_coins = seed_data['coins']
    all_duties = seed_data['duties']
    
@pytest.fixture()
def full_database():
    
    db.connect()
    
    db.create_tables([Coin, Duty, Coin.duties.get_through_model()])
    Coin.insert_many(all_coins).execute()
    Duty.insert_many(all_duties).execute()
    
    yield
    
    db.drop_tables([Coin, Duty, Coin.duties.get_through_model()])
    
    if not db.is_closed():
        db.close()

def test_coins_route_returns_a_list(full_database):
    response = client.get("/coins")
    data = response.json()
    assert isinstance(data, list)

def test_coins_route_returns_5_coins(full_database):
    response = client.get("/coins")
    coin_list = response.json()
    assert len(coin_list) == 5
    
def test_first_coin_is_instance_of_coin(full_database):
    response = client.get("/coins")
    first_coin = response.json()[0]
    assert isinstance(first_coin, Coin)