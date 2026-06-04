from peewee import *
from database import db

class BaseModel(Model):
    class Meta:
        database = db
        schema = 'coins'

class Coin(BaseModel):
    id = AutoField(column_name='coin_id', primary_key=True)
    coin_name = TextField()
    
    class Meta:
        table_name = 'coins'
    
        
class Duty(BaseModel):
    id = AutoField(column_name='duty_id', primary_key=True)
    description = TextField()
    
    class Meta:
        table_name = 'duties'