from flask import Flask
from flask_cors import CORS
from app.models import setup_db


def create_app(config):
    _app = Flask(__name__)
    _app.config.from_pyfile(config)
    return _app


app = create_app('config.py')
CORS(app)
setup_db(app)
