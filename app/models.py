from sqlalchemy import Column
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from app.config import SQLALCHEMY_DATABASE_URI

database_path = SQLALCHEMY_DATABASE_URI
db = SQLAlchemy()


# setup_db(app)
# binds a flask application and a SQLAlchemy service
def setup_db(app):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    Migrate(app, db)
    db.init_app(app)
    db.create_all()


# Movie
# - title
# - release year
class Movie(db.Model):
    __tablename__ = 'Movie'

    id = Column(db.Integer, primary_key=True)
    title = Column(db.String(120), nullable=False)
    release = Column(db.DateTime, nullable=False)

    def __repr__(self):
        return f'<Movie id:{self.id} title: {self.title} release:{self.release}>'


# Actor
# - name
# - date of birth
# - gender
class Actor(db.Model):
    __tablename__ = 'Actor'

    id = Column(db.Integer, primary_key=True)
    name = Column(db.String(120), nullable=False)
    birthdate = Column(db.DateTime, nullable=False)
    gender = Column(db.String(20), nullable=False)

    def __repr__(self):
        return f'<Actor id:{self.id} name: {self.name} birthdate:{self.birthdate} gender:{self.gender}>'
