# Casting Agency API

## Getting Started

### Installing Dependencies

#### Python 3.9

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/index.html)

#### Virtual Environment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virtual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by navigating to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/) and [Psycopg](https://www.psycopg.org/docs/) is a library and adapter to handle the PostgreSQL database.

- [Flask-Migrate](https://flask-migrate.readthedocs.io/) is an extension that handles SQLAlchemy database migrations for Flask applications using Alembic.

- [jose](https://python-jose.readthedocs.io/en/latest/) JavaScript Object Signing and Encryption for JWTs. Useful for encoding, decoding, and verifying JWTS.

### Create the database
```bash
createdb cagency
```

## Running the server

From within the main directory first ensure you are working using your created virtual environment. Run:

```bash
python run.py
```

### Testing
To run the tests, run
```bash
dropdb cagency_test
createdb cagency_test
psql cagency_test < cagency.psql
python app/test_app.py
```

## Endpoints

...

### Heroku Server

...
