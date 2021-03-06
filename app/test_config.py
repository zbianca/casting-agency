import os

SECRET_KEY = os.environ['SECRET_KEY']
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

# Database URL
SQLALCHEMY_DATABASE_URI = os.environ['TEST_DATABASE_URL']

# Disable tracking modifications of objects and emit signals (default = None)
SQLALCHEMY_TRACK_MODIFICATIONS = False

