from peewee import PostgresqlDatabase
from os import getenv

db = PostgresqlDatabase(
    'joe',
    user=getenv('DB_USER'),
    host=getenv('DB_HOST'),
    port=getenv('DB_PORT'),
    password=getenv('DB_PASSWORD')
    )