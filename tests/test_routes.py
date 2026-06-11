from app import app
from fastapi.testclient import TestClient
from src.database import db
import pytest, json
from src.models import Coin, Duty
import os, logging

if os.getenv('DB_LOGGING') == 'on':
    logging.getLogger('peewee').addHandler(logging.StreamHandler())
    logging.getLogger('peewee').setLevel(logging.DEBUG)


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
    
def test_first_coin_has_coin_name_and_id(full_database):
    response = client.get("/coins")
    first_coin = response.json()[0]
    print(first_coin)
    assert 'coin_name' in first_coin
    assert 'id' in first_coin
    
    