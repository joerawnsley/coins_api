import json, os
from src.database import db
from src.models import Coin, Duty

db_location = os.getenv('DB_LOCATION')
remote_schema = os.getenv('REMOTE_SCHEMA')

if not (db_location == 'remote' and remote_schema == 'prod'):
    raise Exception('must set db location to remote and remote schema to prod before seeding')


with open('seed_data/seed_data.json') as json_data:
    seed_data = json.load(json_data)
    all_coins = seed_data['coins']
    all_duties = seed_data['duties']

db.connect()

db.drop_tables([Coin, Duty, Coin.duties.get_through_model()])

db.create_tables([Coin, Duty, Coin.duties.get_through_model()])
Coin.insert_many(all_coins).execute()
Duty.insert_many(all_duties).execute()

if not db.is_closed():
    db.close()