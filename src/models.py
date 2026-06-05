from peewee import *
from src.database import db
import os, dotenv, uuid

dotenv.load_dotenv()

dev_schema = 'coins-dev'
prod_schema = 'coins-prod'

if os.getenv('REMOTE_SCHEMA') == 'PROD':
    current_schema = prod_schema
if os.getenv('REMOTE_SCHEMA') == 'DEV':
    current_schema = dev_schema

class BaseModel(Model):
    class Meta:
        database = db
        if os.getenv('DB_LOCATION') == 'REMOTE':
            schema = current_schema

class Coin(BaseModel):
    id = UUIDField(column_name='coin_id', default=uuid.uuid4, primary_key=True)
    coin_name = TextField()
    
    class Meta:
        table_name = 'coins'
    
        
class Duty(BaseModel):
    id = UUIDField(column_name='duty_id', default=uuid.uuid4, primary_key=True)
    description = TextField()
    duty_number = IntegerField()
    
    class Meta:
        table_name = 'duties'