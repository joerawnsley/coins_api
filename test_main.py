from database import db
from models import Coin, Duty
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
    assert coin.id == 1
    assert coin.coin_name == 'Automate'

def test_add_a_duty(empty_database):
    Duty.insert(duty_name='Duty 1', description='Script and code').execute()
    duty = Duty.get_by_id(1)
    print(f'name: {duty.duty_name}, id: {duty.id}, description: {duty.description}')
    assert duty.id == 1
    assert 'code' in duty.description