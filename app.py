from fastapi import FastAPI
from src.models import Coin, Duty
from src.database import db
from pydantic import BaseModel




app = FastAPI()

# -----welcome endpoint-----
@app.get("/")
def root():
    return {"message": "Welcome to the Coins API"}

# -----coin routes-----

class NewCoin(BaseModel):
    coin_name: str
    coin_path: str
    duties: list[int] | None = None
    is_complete: bool | None = None


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

@app.post("/coins")
def add_coin(coin: NewCoin):
    Coin.create(
        coin_name=coin.coin_name,
        coin_path=coin.coin_path
    )
    if coin.duties:
        saved_coin = Coin.get(Coin.coin_name == coin.coin_name)
        for number in coin.duties:
            saved_coin.duties.add(Duty.get(Duty.duty_number == int(number)))

@app.get("/coins/{coin_path}")
def single_coin():
    pass

@app.put("/coins/{coin_path}")
def update_coin():
    pass

# -----duties routes-----

@app.get("/duties")
def list_duties():
    pass

@app.get("/duties/{duty_number}")
def single_duty():
    pass

@app.post("/duties")
def add_duty():
    pass

@app.put("/duties/{duty_number}")
def update_duty():
    pass