# Coins API

The coins API is an API that returns apprenticeship coins, and allows them to be marked as complete to track progress against the standard
<!-- what else does it do? placeholder -->

## Running/testing locally

### Prerequisites

Requires python 3.12 and pip package manager

### Setting up the environment

create a virtual environment by running the following command from the project root directory

``` python3 -m venv .venv ```

activate the virtual environment

``` source .venv/bin/activate```

install the requirements

``` pip install -r requirements.txt ```

Create a .env file in the project root, and paste in the following text, replacing the values for DB_HOST and DB_PASSWORD with your connection string and password:
```
DB_HOST=[your Digital Ocean connection string]
DB_PASSWORD=[your Digital Ocean DB passowrd]
DB_LOCATION=remote
REMOTE_SCHEMA=prod
DB_LOGGING=off
```

- DB_LOCATION can be set to 'local' allowing you to run the tests against a local sqlite database for speed, or 'remote', allowing you to use your hosted cloud database
- REMOTE_SCHEMA can be 'test' or 'prod'. If DB_LOCATION is 'remote', 'test' will let you run automated tests against the cloud database, while 'prod' will let you run the server and send requests manually
- DB_LOGGING= can be 'on' to show detailed database query logging during tests, 'off' to not show

### Running the tests

To run the tests, ensure REMOTE_SCHEMA is set to ```test``` in you .env file. Run

```pytest```

in the terminal. 
- Do not run tests when remote schema is set to 'prod'
- DB_LOCATION in the .env file can be set to 'local' allowing you to run the tests against a local sqlite database for speed, or 'remote', allowing you to use your hosted cloud database

### Running the server

If you want to add some coins and duties to the database in order to test manually, you can add them (if they haven't already been added) by running the following command from the project root:

```python3 seed_prod_db.py```

The app uses port 8000. To start a local server, run:

```fastapi dev src/app.py```

 ## Deployment

 <!-- placeholder for deployment instructions -->

  ## Calling the API

 <!-- placeholder for usage instructions -->