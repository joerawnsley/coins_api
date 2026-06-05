from peewee import PostgresqlDatabase, SqliteDatabase
import os, dotenv

dotenv.load_dotenv()

postgres_db = PostgresqlDatabase(
    'joe',
    user='joe',
    port=25060,
    host=os.getenv('DB_HOST'),
    password=os.getenv('DB_PASSWORD')
    )

sqlite_db = SqliteDatabase(':memory:')

if os.getenv('DB_LOCATION') == 'REMOTE':
    db = postgres_db
if os.getenv('DB_LOCATION') == 'MEMORY':
    db = sqlite_db