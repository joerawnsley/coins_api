# Coins API

The coins API is an API that returns apprenticeship coins, and allows them to be marked as complete to track progress against the standard
<!-- what else does it do? placeholder -->

## Running/testing locally

### Prerequisites

Requires python 3.12 and pip package manager

### Setting up the environment

Clone this repository and navigate to the project root:

```
git clone https://github.com/joerawnsley/coins_api.git
cd coins_api
```

Create a virtual environment by running the following command from the project root directory

``` python3 -m venv .venv ```

Activate the virtual environment

``` source .venv/bin/activate```

Install the requirements

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

You will get a link to the application running on localhost:8000. See below for a list of available API endpoints.

## Deployment

The Coins API is automatically deployable on AWS using terraform. If you would like to deploy the API in this way, first complete the pre-requisites.

### Pre-requisites

1. Get the app running locally (see above)
2. Install Terraform (version 14.6 used for testing)
3. Have an AWS account
3. Sign into your AWS account via the AWS CLI

### Building the infrastructure

Once you have installed Terraform and authenticated using the AWS CLI, run:

```terraform apply```

Check the plan, and type ```yes``` to accept.

### Deploying the code

Once you have successfully built the infrastructure, there are two ways to deploy the API:
1. Deploy on push: 
    - commit and push a change to the repo, and it will deploy automatically
2. Deploy manually on Github: 
    - open the Github repository in your browser, and click the "Actions" tab. 
    - In the left sidebar, click "build and deploy"
    - in the blue horizontal bar, click "Run worklfow"
    - ensure the "main" branch is selected, then click "Run Workflow"


### Getting the public IP

In the project root, run the folowing commands in the terminal:
```
chmod +x get-public-ip.sh
```
then
```
./get-public-ip.sh
```
The public IP should appear in your terminal

Note: if you have just deployed the app, wait for the deployment to complete before getting the public IP. This can take up to 10 minutes.

## Endpoints

Once the app is deployed or running locally, API calls are made to 
```
http://<IP address>:8000/<endpoint>
```

for example, if your IP address is 127.0.0.1, send a request to:

```http://127.0.0.1:8000/``` for the welcome page, or

```http://127.0.0.1/coins/automate``` for the automate coin details.

The following endpoints are available:

### GET endpoints

- ```/``` returns a welcome message
- ```/coins``` returns a list of all coins
- ```/coins/<coin path>``` returns information about a specific coin. Coin path are a shortened form of a coin's name. List all coins to see the available coin paths
- ```/duties``` returns a listof all duties
- ```/duties/<duty_number>``` returns information about a specific duty

### POST endpoints

- ```/coins``` creates a new coin. Pass in the coin as JSON in the request body. For example:

    ```
        # POST request body:
        {
            "coin_name": "Going Deeper",
            "coin_path": "deeper"
        }
    ```
    The following fields are available:
    - "coin_name": (string, required)
    - "coin_path": (string, required, must be unique)
    - "duties": (list of integers, optional, must reference duties currently in the database by their duty_number)
    - "is_complete": (boolean, defaults to false if omitted)

- ```/duties``` creates a new duty. Pass in the duty as JSON in the request body. For example:

    ```
    # POST request body
    {
        "duty_number": 1,
        "description": "Script and code"
    }
    ```

    Only two fields are available:
    - "duty_number": (integer, required, must be unique)
    - "description": (string, required)



