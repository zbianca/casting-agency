from flask import Flask
from flask_cors import CORS
from app.routes import routes
from app.models import setup_db


def create_app(config):
    _app = Flask(__name__)
    _app.config.from_pyfile(config)
    _app.register_blueprint(routes)

    return _app


app = create_app('config.py')
CORS(app)
setup_db(app)
