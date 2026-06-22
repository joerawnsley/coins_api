from peewee import *
from database import db
import os, dotenv, uuid

dotenv.load_dotenv()

test_schema = 'coins-dev'
prod_schema = 'coins-prod'

if os.getenv('REMOTE_SCHEMA') == 'prod':
    current_schema = prod_schema
if os.getenv('REMOTE_SCHEMA') == 'test':
    current_schema = test_schema

class BaseModel(Model):
    class Meta:
        database = db
        if os.getenv('DB_LOCATION') == 'remote':
            schema = current_schema

class Duty(BaseModel):
    id = UUIDField(column_name='duty_id', default=uuid.uuid4, primary_key=True)
    description = TextField()
    duty_number = IntegerField(unique=True)
    
    class Meta:
        table_name = 'duties'

class Coin(BaseModel):
    id = UUIDField(column_name='coin_id', default=uuid.uuid4, primary_key=True)
    coin_name = TextField(unique=True)
    coin_path = TextField(unique=True)
    duties = ManyToManyField(Duty, backref='coins')
    is_complete = BooleanField(default=False)
    
    class Meta:
        table_name = 'coins'