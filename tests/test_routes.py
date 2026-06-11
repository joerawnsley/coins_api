from app import app
from fastapi.testclient import TestClient
from src.database import db
from src.utils import is_valid_uuid
import pytest, json, peewee
from src.models import Coin, Duty
import os, logging

if os.getenv('DB_LOGGING') == 'on':
    logging.getLogger('peewee').addHandler(logging.StreamHandler())
    logging.getLogger('peewee').setLevel(logging.DEBUG)

# ------------ create test client ----------------
client = TestClient(app)

# --------------- test fixtures -----------------
@pytest.fixture()
def empty_database():
    with db:
        db.create_tables([Coin, Duty, Coin.duties.get_through_model()])
        
        yield
        
        db.drop_tables([Coin, Duty, Coin.duties.get_through_model()])

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

# ----- welcome endpoint -----

def test_root_returns_message():
    response = client.get("/")
    assert response.status_code == 200
    assert "Welcome" in response.text

def test_root_returns_json_object():
    response = client.get("/")
    data = response.json()
    assert isinstance(data, dict)

# ----- get /coins -----

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
    assert 'coinName' in first_coin
    assert 'id' in first_coin

def test_all_coins_have_coin_name_and_id(full_database):
    response = client.get("/coins")
    coin_list = response.json()
    for coin in coin_list:
        assert 'coinName' in coin
        assert 'id' in coin

def test_data_types_in_coin(full_database):
    response = client.get("/coins")
    coin_3 = response.json()[3]
    print(coin_3)
    assert type(coin_3['coinName'] == str)
    assert is_valid_uuid(coin_3['id'])
    assert type(coin_3['duties']) == list
    assert type(coin_3['isComplete']) == bool
    
# -------- post /coins --------

def test_add_coin_to_empty_db(empty_database):
    
    assert Coin.select().where(Coin.coin_path == 'deeper').first() is None

    coin_data = {
        "coin_name": "Going Deeper",
        "coin_path": "deeper",
        "duties": [11]
    }
    response = client.post("/coins", json=coin_data)
    
    assert response.status_code == 200
    assert Coin.select().where(Coin.coin_path == 'deeper').first() is not None

    
    

