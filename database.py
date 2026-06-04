from peewee import PostgresqlDatabase
import os, dotenv

dotenv.load_dotenv()

db = PostgresqlDatabase(
    'joe',
    user=os.getenv('DB_USER'),
    host=os.getenv('DB_HOST'),
    port=os.getenv('DB_PORT'),
    password=os.getenv('DB_PASSWORD')
    )