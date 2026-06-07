from src.database import db
from src.models import Coin, Duty
from src.utils import is_valid_uuid
import pytest, json

import logging
logging.getLogger('peewee').addHandler(logging.StreamHandler())
logging.getLogger('peewee').setLevel(logging.DEBUG)

# -------- connection test --------
def test_connection():
    connection = db.connect()
    print(connection)
    assert connection
    if not db.is_closed():
        db.close()

# -------- empty database tests --------
@pytest.fixture()
def empty_database():
    with db:
        db.create_tables([Coin, Duty, Coin.duties.get_through_model()])
        
        yield
        
        db.drop_tables([Coin, Duty, Coin.duties.get_through_model()])

def test_coin_table_is_empty(empty_database):
    
    coins = Coin.select()
    assert list(coins) == []
    
def test_add_a_coin(empty_database):
    Coin.insert(coin_name='Automate').execute()
    coin = Coin.select().first()
    print(f'name: {coin.coin_name}, id: {coin.id}')
    assert is_valid_uuid(coin.id)
    assert coin.coin_name == 'Automate'

def test_add_a_duty(empty_database):
    Duty.insert(duty_number=1, description='Script and code').execute()
    duty = Duty.select().first()
    print(f'name: {duty.duty_number}, id: {duty.id}, description: {duty.description}')
    assert is_valid_uuid(duty.id)
    assert 'code' in duty.description
    assert type(duty.duty_number) is int

# -------- full database tests --------

with open('seed_data/seed_data.json') as json_data:
    seed_data = json.load(json_data)
    all_coins = seed_data['coins']
    all_duties = seed_data['duties']
    
@pytest.fixture()
def full_database():
    with db:
        db.create_tables([Coin, Duty, Coin.duties.get_through_model()])
        Coin.insert_many(all_coins).execute()
        Duty.insert_many(all_duties).execute()
        
        yield
        
        db.drop_tables([Coin, Duty, Coin.duties.get_through_model()])
        
def test_5_coins_exist(full_database):
    for coin in Coin.select():
        print(coin.coin_name)
    assert Coin.select().count() == 5

def test_13_duties_exist(full_database):
    assert Duty.select().count() == 13
    
def test_assemble_coin_exists(full_database):
    assemble = Coin.select().where(Coin.coin_name == 'Assemble')
    assert assemble.exists()

def test_duty_10_is_monitoring(full_database):
    duty_10 = Duty.get(Duty.duty_number == 10)
    print(duty_10.description)
    assert "monitoring" in duty_10.description
    
def test_duty_8_is_architecture(full_database):
    duty_8 = Duty.get(Duty.duty_number == 8)
    print(duty_8.description)
    assert "architecture" in duty_8.description

# ------ test duties can be added to coins ---------------

def test_add_duty_to_coin(full_database):
    assemble = Coin.get(Coin.coin_name == 'Assemble')
    assemble_duties = [duty.duty_number for duty in assemble.duties]
    print(assemble_duties)
    assert len(assemble_duties) == 0
    
    duty_8 = Duty.get(Duty.duty_number == 8)
    assemble.duties.add(duty_8)
    
    assemble_duties = [duty.duty_number for duty in assemble.duties]
    print(assemble_duties)
    assert len(assemble_duties) == 1
    assert 8 in assemble_duties
    assert 7 not in assemble_duties
    
def test_add_two_duties_to_coin(full_database):
    houston = Coin.get(Coin.coin_name == "Houston, Prepare to Launch")
    houston_duties = [duty.duty_number for duty in houston.duties]
    assert len(houston_duties) == 0
    
    duty_5 = Duty.get(Duty.duty_number == 5)
    duty_7 = Duty.get(Duty.duty_number == 7)
    duty_10 = Duty.get(Duty.duty_number == 10)
    houston.duties.add([duty_5, duty_7, duty_10])
    
    houston_duties = [duty.duty_number for duty in houston.duties]
    print(houston_duties)
    assert 5 in houston_duties; assert 7 in houston_duties; assert 10 in houston_duties
    assert len(houston_duties) == 3
    