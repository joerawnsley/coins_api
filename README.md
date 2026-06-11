Variables to include in .env:

- DB_HOST=[your Digital Ocean connection string]
- DB_PASSWORD=[your Digital Ocean DB passowrd]
- DB_LOCATION=['remote' to use remote db, 'local' for local testing]
- REMOTE_SCHEMA=['dev' for integration testing, 'prod' for production]
- DB_LOGGING=['on' to show detailed query logging during tests, 'off' to not show]

Do not run tests when remote schema is set to 'prod'