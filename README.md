# Casting Agency API

### Heroku Server
~~Project hosted in heroku: https://casting-agency-bz.herokuapp.com~~

## Getting Started

### Installing Dependencies

#### Python 3.9

Follow instructions to install the latest version of python for your platform in
the [python docs](https://docs.python.org/3/using/index.html)

#### Virtual Environment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for
each project separate and organized. Instructions for setting up a virtual environment for your platform can be found in
the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by navigating to the `/backend` directory
and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle
  requests and responses.

- [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/) and [Psycopg](https://www.psycopg.org/docs/) is a
  library and adapter to handle the PostgreSQL database.

- [Flask-Migrate](https://flask-migrate.readthedocs.io/) is an extension that handles SQLAlchemy database migrations for
  Flask applications using Alembic.

- [jose](https://python-jose.readthedocs.io/en/latest/) JavaScript Object Signing and Encryption for JWTs. Useful for
  encoding, decoding, and verifying JWTS.

### Create the database

```bash
createdb cagency
```

## Running the server

On your first local run, source the setup.sh file. It defines shell environment variables necessary for the project. Run:
```bash
source setup.sh
```

From within the main directory first ensure you are working using your created virtual environment. Run:

```bash
python run.py
```

### Testing

To run the tests, run

```bash
dropdb cagency_test
createdb cagency_test
python test_app.py
```

The repository has a Postman collection file, in which tokens were not included. Please edit the tokens on the json file before using the collection to test the endpoints. 

## Endpoints

### GET `/actors`
Response:
```json
{
    "actors": [{
            "age": 45,
            "dob": "19. July 1976",
            "gender": "m",
            "id": 1,
            "name": "Benedict Cumberbatch"
        }]
}
```

### GET `/movies`
Response:
```json
{
    "movies": [
        {
            "id": 1,
            "release": "Sunday, 22. April 2001",
            "title": "Shrek"
        },
        {
            "id": 2,
            "release": "Friday, 26. October 1984",
            "title": "The Terminator"
        }]
}
```

### DELETE `/actors/<id>`
Response:
```json
{
    "deleted": 4,
    "success": true
}
```
### DELETE `/movies/<id>`
Response:
```json
{
    "deleted": 1,
    "success": true
}
```
### POST `/actors`
Request body (json):
```json
{
  "name": "Benedict Cucumberbatch",
  "birthdate": "1976-07-19",
  "gender": "m"
}
```
Response:
```json
{
    "added": {
        "age": 45,
        "dob": "19. July 1976",
        "gender": "m",
        "id": 1,
        "name": "Benedict Cucumberbatch"
    },
    "success": true
}
```
### POST `/movies`
Request body (json):
```json
{
  "title": "Terminator",
  "release": "1984-10-26"
}
```
Response:
```json
{
    "added": {
        "id": 5,
        "release": "Friday, 26. October 1984",
        "title": "Terminator"
    },
    "success": true
}
```
### PATCH `/actors/<id>`
Request body (json):
```json
{
  "name": "Benedict Cumberbatch",
  "birthdate": "1976-07-19",
  "gender": "m"
}
```
Response:
```json
{
    "success": true,
    "updated": {
        "age": 45,
        "dob": "19. July 1976",
        "gender": "m",
        "id": 1,
        "name": "Benedict Cumberbatch"
    }
}
```
### PATCH `/movies/<id>`
Request body (json):
```json
{
  "title": "Pulp Fiction",
  "release": "1994-05-21"
}
```
Response:
```json
{
    "success": true,
    "updated": {
        "id": 4,
        "release": "Saturday, 21. May 1994",
        "title": "Pulp Fiction"
    }
}
```
### Auth0

Authentication route: `/login`

#### Roles:
- Assistant
  * Can view actors and movies
- Director
  * All permissions a Casting Assistant has and…
  * Add or delete an actor from the database
  * Modify actors or movies
- Producer
  * All permissions a Casting Director has and…
  * Add or delete a movie from the database
