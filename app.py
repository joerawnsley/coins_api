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
        coin_name = coin.coin_name,
        duties = [duty.duty_number for duty in coin.duties],
        is_complete = coin.is_complete
    ))
    return coin_list



# @app.get("/coins")
# def list_coins():
#     query = Coin.select().dicts()
#     coin_list = [coin for coin in query]
#     for coin in coin_list:
#         coin["duties"] = []
#     return coin_list

