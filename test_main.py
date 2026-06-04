from database import db
from models import Coin, Duty

def test_connection():
    connection = db.connect()
    assert connection
    if not db.is_closed():
        db.close()

def test_pull_coin_from_db():
    with db:
        first_coin = Coin.select().first()
        print(first_coin.coin_name)
        assert first_coin
    if not db.is_closed():
        db.close()
    
def test_pull_duty_from_db():
    with db:
        first_duty = Duty.select().first()
        print(first_duty.description)
        assert first_duty
    if not db.is_closed():
        db.close()