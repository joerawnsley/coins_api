from peewee import PostgresqlDatabase, SqliteDatabase
import os, dotenv

dotenv.load_dotenv()

remote_postgres_db = PostgresqlDatabase(
    'joe',
    user='joe',
    port=25060,
    host=os.getenv('DB_HOST'),
    password=os.getenv('DB_PASSWORD')
    )

sqlite_db = SqliteDatabase('local.db')

if os.getenv('DB_LOCATION') == 'remote':
    db = remote_postgres_db
if os.getenv('DB_LOCATION') == 'local':
    db = sqlite_db