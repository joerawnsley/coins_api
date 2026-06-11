from fastapi import FastAPI
from src.models import Coin
from src.database import db

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Welcome to the Coins API"}

@app.get("/coins")
def list_coins():
    coin = Coin.select().dicts()[0]
    return [coin, {}, {}, {}, {}]