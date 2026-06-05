from peewee import PostgresqlDatabase, SqliteDatabase
import os, dotenv

dotenv.load_dotenv()

postgres_db = PostgresqlDatabase(
    'joe',
    user=os.getenv('DB_USER'),
    host=os.getenv('DB_HOST'),
    port=os.getenv('DB_PORT'),
    password=os.getenv('DB_PASSWORD')
    )

sqlite_db = SqliteDatabase(':memory:')

if os.getenv('DB_LOCATION') == 'REMOTE':
    db = postgres_db
if os.getenv('DB_LOCATION') == 'MEMORY':
    db = sqlite_db