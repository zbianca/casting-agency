import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from app.models import setup_db, Actor, Movie

TKN_ASSISTANT = f'Bearer %s' % (os.environ['ASSISTANT'])
TKN_DIRECTOR = f'Bearer %s' % (os.environ['DIRECTOR'])
TKN_PRODUCER = f'Bearer %s' % (os.environ['PRODUCER'])
TEST_DATABASE_URI = os.environ['TEST_DATABASE_URL']

first_actor = {
    "name": "Cameron Diaz",
    "birthdate": "1972-08-30",
    "gender": "f"
}

first_movie = {
  "title": "Shrek",
  "release": "2001-05-18"
}

new_actor = {
    "name": "Benedict Cucumberbatch",
    "birthdate": "1976-07-19",
    "gender": "m"
}

incomplete_actor = {
    "name": "Benedict Cumberbatch",
    "gender": "m"
}

patched_actor = {
    "name": "Benedict Cumberbatch",
    "birthdate": "1976-07-19",
    "gender": "m"
}

new_movie = {
  "title": "Terminator",
  "release": "1984-10-26"
}

incomplete_movie = {
  "title": "Terminator"
}

patched_movie = {
  "title": "The Terminator",
  "release": "1984-10-26"
}


class CagencyTestCase(unittest.TestCase):

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app('test_config.py')
        self.client = self.app.test_client
        self.database_name = "cagency_test"
        self.database_path = TEST_DATABASE_URI
        setup_db(self.app)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()

        self.client().post(
            '/actors',
            json=first_actor,
            headers={"Content-Type": 'application/json', "Authorization": TKN_PRODUCER}
        )

        self.client().post(
            '/movies',
            json=first_movie,
            headers={"Content-Type": 'application/json', "Authorization": TKN_PRODUCER}
        )

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_200_insert_actor(self):
        res = self.client().post(
            '/actors',
            json=new_actor,
            headers={"Content-Type": 'application/json', "Authorization": TKN_DIRECTOR}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['added']['name'], 'Benedict Cucumberbatch')

    def test_422_insert_incomplete_actor(self):
        res = self.client().post(
            '/actors',
            json=incomplete_actor,
            headers={"Content-Type": 'application/json', "Authorization": TKN_DIRECTOR}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'unprocessable')

    def test_403_actor_insertion_not_allowed(self):
        res = self.client().post(
            '/actors',
            json=new_actor,
            headers={"Content-Type": 'application/json', "Authorization": TKN_ASSISTANT}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Not allowed.')

    def test_200_retrieve_actors(self):
        res = self.client().get(
            '/actors',
            headers={"Content-Type": 'application/json', "Authorization": TKN_ASSISTANT}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['actors'])
        self.assertTrue(len(data['actors']))

    def test_401_retrieve_actors_header_missing(self):
        res = self.client().get(
            '/actors',
            headers={"Content-Type": 'application/json'}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])
        self.assertNotIn('actors', data)

    def test_200_update_actor(self):
        res = self.client().patch(
            '/actors/2',
            json=patched_actor,
            headers={"Content-Type": 'application/json', "Authorization": TKN_DIRECTOR}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['updated']['name'], 'Benedict Cumberbatch')

    def test_403_update_actor_not_allowed(self):
        res = self.client().patch(
            '/actors/2',
            json=patched_actor,
            headers={"Content-Type": 'application/json', "Authorization": TKN_ASSISTANT}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Not allowed.')

    def test_200_delete_actor(self):
        res = self.client().delete(
            '/actors/1',
            headers={"Content-Type": 'application/json', "Authorization": TKN_PRODUCER}
        )
        data = json.loads(res.data)

        actor = Actor.query.filter(Actor.id == 1).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(actor, None)

    def test_404_cannot_delete_actor_not_found(self):
        res = self.client().delete(
            '/actors/1234',
            headers={"Content-Type": 'application/json', "Authorization": TKN_DIRECTOR}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Actor not found to be deleted')

    def test_200_insert_movie(self):
        res = self.client().post(
            '/movies',
            json=new_movie,
            headers={"Content-Type": 'application/json', "Authorization": TKN_PRODUCER}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['added']['title'], 'Terminator')

    def test_422_insert_incomplete_movie(self):
        res = self.client().post(
            '/movies',
            json=incomplete_movie,
            headers={"Content-Type": 'application/json', "Authorization": TKN_PRODUCER}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'unprocessable')

    def test_403_movie_insertion_not_allowed(self):
        res = self.client().post(
            '/movies',
            json=new_movie,
            headers={"Content-Type": 'application/json', "Authorization": TKN_DIRECTOR}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Not allowed.')

    def test_200_retrieve_movies(self):
        res = self.client().get(
            '/movies',
            headers={"Content-Type": 'application/json', "Authorization": TKN_ASSISTANT}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['movies'])
        self.assertTrue(len(data['movies']))

    def test_401_retrieve_movies_header_missing(self):
        res = self.client().get(
            '/movies',
            headers={"Content-Type": 'application/json'}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])
        self.assertNotIn('movies', data)

    def test_200_update_movie(self):
        res = self.client().patch(
            '/movies/2',
            json=patched_movie,
            headers={"Content-Type": 'application/json', "Authorization": TKN_DIRECTOR}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['updated']['title'], 'The Terminator')

    def test_403_update_movie_not_allowed(self):
        res = self.client().patch(
            '/movies/2',
            json=patched_movie,
            headers={"Content-Type": 'application/json', "Authorization": TKN_ASSISTANT}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Not allowed.')

    def test_200_delete_movie(self):
        res = self.client().delete(
            '/movies/1',
            headers={"Content-Type": 'application/json', "Authorization": TKN_PRODUCER}
        )
        data = json.loads(res.data)

        movie = Movie.query.filter(Movie.id == 1).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(movie, None)

    def test_404_cannot_delete_movie_not_found(self):
        res = self.client().delete(
            '/movies/1234',
            headers={"Content-Type": 'application/json', "Authorization": TKN_PRODUCER}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Movie not found to be deleted')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
