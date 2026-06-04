from main import db

def test_connection():
    print(db)
    assert db