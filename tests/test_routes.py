from src.app import app
from fastapi.testclient import TestClient
from src.database import db
from src.utils import is_valid_uuid, coin_to_dict
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
    db.connect()
    db.create_tables([Coin, Duty, Coin.duties.get_through_model()])
    
    yield
    
    db.drop_tables([Coin, Duty, Coin.duties.get_through_model()])
    if not db.is_closed():
        db.close()

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

@pytest.fixture()
def db_with_duties_but_no_coins():
    
    db.connect()
    db.create_tables([Coin, Duty, Coin.duties.get_through_model()])
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
    assert type(coin_3['coinName'] == str)
    assert is_valid_uuid(coin_3['id'])
    assert type(coin_3['duties']) == list
    assert type(coin_3['isComplete']) == bool
    
# -------- post /coins --------

def test_add_coin_with_no_duties_to_empty_db(empty_database):
    
    assert Coin.select().where(Coin.coin_path == 'deeper').first() is None

    coin_data = {
        "coin_name": "Going Deeper",
        "coin_path": "deeper",
    }
    response = client.post("/coins", json=coin_data)
    
    assert response.status_code == 201
    assert Coin.select().where(Coin.coin_path == 'deeper').first() is not None

    
def test_add_coin_with_duties(db_with_duties_but_no_coins):
    
    assert Coin.select().where(Coin.coin_path == 'deeper').first() is None

    coin_data = {
        "coin_name": "Going Deeper",
        "coin_path": "deeper",
        "duties": ["11", "12"]
    }
    response = client.post("/coins", json=coin_data)
    
    assert response.status_code == 201
    assert Coin.select().where(Coin.coin_path == 'deeper').first() is not None
    
    new_coin = Coin.get(Coin.coin_path == "deeper")
    new_coin_duties = [duty.duty_number for duty in new_coin.duties.order_by(Duty.duty_number)]
    assert new_coin_duties[0] == 11
    assert len(new_coin_duties) == 2


def test_coin_detail_page_gets_a_single_coin(full_database):
    
    assemble_coin = Coin.get(Coin.coin_path == 'assemble')
    duty_8 = Duty.get(Duty.duty_number == 8)
    assemble_coin.duties.add(duty_8)
    
    response = client.get("/coins/assemble")
    data = response.json()
    
    assert type(data) == dict
    assert data["coinName"] == "Assemble"
    assert data["duties"][0] == 8
    
def test_add_coin_returns_201(db_with_duties_but_no_coins):
    
    coin_data = {
        "coin_name": "Going Deeper",
        "coin_path": "deeper",
        "duties": ["11", "12"]
    }
    response = client.post("/coins", json=coin_data)
    
    assert response.status_code == 201
    
# add duties to coin
def test_add_duty_to_coin(full_database):
    automate_coin = Coin.get(Coin.coin_path == 'automate')
    automate_duties = [duty.duty_number for duty in automate_coin.duties]
    
    print("AUTOMATE COIN", coin_to_dict(automate_coin))
    print(automate_duties)
    assert automate_coin.duties == []
    
    client.put("/coins/automate/add-duties", json = [1, 2, 3])
    assert automate_duties == [1, 2, 3]
    
    
# duties routes

def test_duties_route_returns_12_duties(full_database):
    response = client.get("/duties")
    duty_list = response.json()
    assert len(duty_list) == 13

def test_all_duties_have_number_and_description(full_database):
    response = client.get("/duties")
    duty_list = response.json()
    for duty in duty_list:
        assert 'dutyNumber' in duty
        assert 'description' in duty