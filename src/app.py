from fastapi import FastAPI
from src.models import Coin, Duty
from src.database import db
from src.utils import coin_to_dict, duty_to_dict
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
        coin_list.append(coin_to_dict(coin))
    return coin_list

@app.post("/coins", status_code=201)
def add_coin(coin: NewCoin):
    Coin.create(
        coin_name=coin.coin_name,
        coin_path=coin.coin_path
    )
    if coin.duties:
        saved_coin = Coin.get(Coin.coin_name == coin.coin_name)
        for number in coin.duties:
            saved_coin.duties.add(Duty.get(Duty.duty_number == int(number)))
    
    created_coin = Coin.get(Coin.coin_path == coin.coin_path)
    return coin_to_dict(created_coin)
    

@app.get("/coins/{coin_path}")
def single_coin(coin_path):
    selected_coin = Coin.get(Coin.coin_path == coin_path)
    return coin_to_dict(selected_coin)

@app.delete("/coins/{coin_path}")
def delete_coin(coin_path):
    Coin.delete().where(Coin.coin_path == coin_path).execute()
    return "Coin deleted"

# for adding and removing duties from coins
@app.put("/coins/{coin_path}/add-duties")
def add_duty_to_coin(coin_path, duties: list[int]):
    selected_coin = Coin.get(Coin.coin_path == coin_path)
    for number in duties:
        selected_coin.duties.add(Duty.get(Duty.duty_number == number))
    return coin_to_dict(selected_coin)


@app.put("/coins/{coin_path}/remove-duties")
def remove_duty_from_coin(coin_path, duties: list[int]):
    selected_coin = Coin.get(Coin.coin_path == coin_path)
    for number in duties:
        selected_coin.duties.remove(Duty.get(Duty.duty_number == number))
    return coin_to_dict(selected_coin)

@app.put("/coins/{coin_path}/mark-complete")
def mark_coin_complete(coin_path):
    selected_coin = Coin.get(Coin.coin_path == coin_path)
    selected_coin.update(is_complete=True).execute()
    updated_coin = Coin.get(Coin.coin_path == coin_path)
    return coin_to_dict(updated_coin)

@app.put("/coins/{coin_path}/mark-incomplete")
def mark_coin_incomplete(coin_path):
    selected_coin = Coin.get(Coin.coin_path == coin_path)
    selected_coin.update(is_complete=False).execute()
    updated_coin = Coin.get(Coin.coin_path == coin_path)
    return coin_to_dict(updated_coin)

# -----duties routes-----

@app.get("/duties")
def list_duties():
    query = Duty.select()
    duty_list = []
    for duty in query:
        duty_list.append(duty_to_dict(duty))
    return duty_list

@app.get("/duties/{duty_number}")
def single_duty(duty_number):
    selected_duty = Duty.get(Duty.duty_number == duty_number)
    return duty_to_dict(selected_duty)

@app.post("/duties")
def add_duty():
    # awaiting implementation
    pass

@app.put("/duties/{duty_number}")
def update_duty():
    # awaiting implementation
    pass

@app.delete("/duties/{duty_number}")
def delete_duty():
    return "Error: Duties are forever. They cannot be deleted."
    
