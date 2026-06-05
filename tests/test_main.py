from src.database import db
from src.models import Coin, Duty
from src.utils import is_valid_uuid
from peewee import SchemaManager
import pytest

def test_connection():
    connection = db.connect()
    print(connection)
    assert connection
    if not db.is_closed():
        db.close()


@pytest.fixture()
def empty_database():
    with db:
        db.create_tables([Coin, Duty])
        
        yield
        
        db.drop_tables([Coin, Duty])

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
    Duty.insert(duty_name='Duty 1', description='Script and code').execute()
    duty = Duty.select().first()
    print(f'name: {duty.duty_number}, id: {duty.id}, description: {duty.description}')
    assert is_valid_uuid(duty.id)
    assert 'code' in duty.description
    assert type(duty.duty_number) is int