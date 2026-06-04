from main import db

def test_connection():
    connection = db.connect()
    assert connection