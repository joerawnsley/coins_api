from fastapi import FastAPI
from src.models import Coin, Duty
from src.database import db
import json

with open('seed_data/seed_data.json') as json_data:
    seed_data = json.load(json_data)
    all_coins = seed_data['coins']
    all_duties = seed_data['duties']

if not db.is_closed():
    db.close()
db.connect()

db.drop_tables([Coin, Duty, Coin.duties.get_through_model()])
db.create_tables([Coin, Duty, Coin.duties.get_through_model()])
Coin.insert_many(all_coins).execute()
Duty.insert_many(all_duties).execute()

# --------------------------------------

automate = Coin.get(Coin.coin_name == 'Automate')
print("get_automate: ", automate)

duty_1 = Duty.get(Duty.duty_number == 1)
duty_2 = Duty.get(Duty.duty_number == 2)
duty_3 = Duty.get(Duty.duty_number == 3)

automate.duties.add([duty_1, duty_2, duty_3])

query = Coin.select()
coin_list = []
for coin in query:
    # duties = [duty.duty_number for duty in coin.duties]
    coin_list.append(dict(
        id = coin.id,
        coin_name = coin.coin_name,
        duties = [duty.duty_number for duty in coin.duties],
        isComplete = coin.is_complete
    ))
    
print("coin_list:", coin_list)

# --------------------------------------

db.drop_tables([Coin, Duty, Coin.duties.get_through_model()])
    
if not db.is_closed():
        db.close()