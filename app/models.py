import datetime
from sqlalchemy import Column
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()


def seed_data():
    first_actor = {
        "name": "Cameron Diaz",
        "birthdate": "1972-08-30",
        "gender": "f"
    }

    first_movie = {
      "title": "Shrek",
      "release": "2001-05-18"
    }

    actor = Actor.query.first()
    movie = Movie.query.first()

    if actor is None:
        actor = Actor(name=first_actor["name"], birthdate=first_actor["birthdate"], gender=first_actor["gender"])
        actor.insert()

    if movie is None:
        movie = Movie(title=first_movie["title"], release=first_movie["release"])
        movie.insert()


# setup_db(app)
# binds a flask application and a SQLAlchemy service
def setup_db(app):
    db.app = app
    Migrate(app, db, compare_type=True)
    db.init_app(app)
    db.create_all()
    seed_data()


# Movie
# - title
# - release year
class Movie(db.Model):
    __tablename__ = 'Movie'

    id = Column(db.Integer, primary_key=True)
    title = Column(db.String(120), nullable=False)
    release = Column(db.Date, nullable=False)

    def __repr__(self):
        return f'<Movie id:{self.id} title: {self.title} release:{self.release}>'

    def short(self):
        return {
            'id': self.id,
            'title': self.title,
            'release': self.release.strftime("%A, %d. %B %Y"),
        }

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def update():
        db.session.commit()


# Actor
# - name
# - date of birth
# - gender
class Actor(db.Model):
    __tablename__ = 'Actor'

    id = Column(db.Integer, primary_key=True)
    name = Column(db.String(120), nullable=False)
    birthdate = Column(db.Date, nullable=False)
    gender = Column(db.String(20), nullable=False)

    def __repr__(self):
        return f'<Actor id:{self.id} name: {self.name} birthdate:{self.birthdate} gender:{self.gender}>'

    def short(self):
        today = datetime.date.today()
        born = self.birthdate
        age = today.year - born.year - ((today.month, today.day) < (born.month, born.day))

        return {
            'id': self.id,
            'name': self.name,
            'dob': self.birthdate.strftime("%d. %B %Y"),
            'age': age,
            'gender': self.gender,
        }

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def update():
        db.session.commit()
