from fastapi import FastAPI
from src.models import Coin
from src.database import db

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Welcome to the Coins API"}


@app.get("/coins")
def list_coins():
    query = Coin.select()
    coin_list = []
    for coin in query:
        coin_list.append(dict(
        id = coin.id,
        coinName = coin.coin_name,
        duties = [duty.duty_number for duty in coin.duties],
        isComplete = coin.is_complete
    ))
    return coin_list