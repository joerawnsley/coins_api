Variables to include in .env:

- DB_HOST=[your Digital Ocean connection string]
- DB_PASSWORD=[your Digital Ocean DB passowrd]
- DB_LOCATION=[REMOTE to use remote db, MEMORY for local testing]
- REMOTE_SCHEMA=[DEV for integration testing, PROD for production]

Do not run tests when remote schema is set to PROD