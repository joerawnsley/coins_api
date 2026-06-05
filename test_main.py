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
def test_database():
    with db:
        db.create_tables([Coin, Duty])
        
        yield
        
        db.drop_tables([Coin, Duty])

def test_coin_table_is_empty(test_database):
    
    coins = Coin.select()
    assert list(coins) == []
    
def test_add_a_coin(test_database):
    Coin.insert(coin_name='Automate').execute()
    coin = Coin.select().first()
    print(f'name: {coin.coin_name}, id: {coin.id}')
    assert coin.id == 1
    assert coin.coin_name == 'Automate'
    