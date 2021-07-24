import json
import markdown
import markdown.extensions.fenced_code
import os
from flask import Blueprint, request, jsonify, abort, redirect
from app.models import Movie, Actor
from app.auth import AuthError, requires_auth

AUTH0_DOMAIN = os.environ['AUTH0_DOMAIN']
ALGORITHMS = os.environ['ALGORITHMS']
API_AUDIENCE = os.environ['API_AUDIENCE']
AUTH0_CLIENT_ID = os.environ['AUTH0_CLIENT_ID']
AUTH0_CALLBACK_URL = os.environ['AUTH0_CALLBACK_URL']

routes = Blueprint('routes', __name__)


# CORS Headers
@routes.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')  # TODO: disallow CORS
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    return response


# render README as index
@routes.route('/')
def index():
    readme_file = open("README.md", "r")
    md_template_string = markdown.markdown(
        readme_file.read(), extensions=["fenced_code"]
    )

    return md_template_string


# redirects to auth0 login page
@routes.route("/login", methods=["GET"])
def generate_auth_url():
    url = f'https://{AUTH0_DOMAIN}/authorize' \
          f'?audience={API_AUDIENCE}' \
          f'&response_type=token&client_id=' \
          f'{AUTH0_CLIENT_ID}&redirect_uri=' \
          f'{AUTH0_CALLBACK_URL}'

    return redirect(url)


# get all actors
@routes.route('/actors', methods=['GET'])
@requires_auth('get:actors')
def get_actors(payload):
    try:
        actors = Actor.query.all()

        if not actors:
            abort(404)

        return jsonify({
            'success': True,
            'actors': [actor.short() for actor in actors]
        }), 200
    except Exception:
        abort(500)


# get all movies
@routes.route('/movies', methods=['GET'])
@requires_auth('get:movies')
def get_movies(payload):
    try:
        movies = Movie.query.all()

        if not movies:
            abort(404)

        return jsonify({
            'success': True,
            'movies': [movie.short() for movie in movies]
        }), 200
    except Exception:
        abort(500)


# Delete Actor by id
@routes.route('/actors/<int:actor_id>', methods=['DELETE'])
@requires_auth('delete:actors')
def delete_actor(payload, actor_id):
    try:
        actor = Actor.query.get(actor_id)

        if not actor:
            return json.dumps({
                'success': False,
                'message': 'Actor not found to be deleted'
            }), 404

        actor.delete()

    except Exception:
        abort(422)

    return jsonify({
        'success': True,
        'deleted': actor_id
    })


# Delete Movie by id
@routes.route('/movies/<int:movie_id>', methods=['DELETE'])
@requires_auth('delete:movies')
def delete_movie(payload, movie_id):
    try:
        movie = Movie.query.get(movie_id)

        if not movie:
            return json.dumps({
                'success': False,
                'message': 'Movie not found to be deleted'
            }), 404

        movie.delete()

    except Exception:
        abort(422)

    return jsonify({
        'success': True,
        'deleted': movie_id
    })


# Add a new actor
@routes.route('/actors', methods=['POST'])
@requires_auth('post:actors')
def create_actor(payload):
    body = request.get_json()
    name = body.get('name', None)
    birthdate = body.get('birthdate', None)  # 'YYYY-MM-DD'
    gender = body.get('gender', 'd')

    if name is None or birthdate is None:
        abort(422)

    try:
        actor = Actor(name=name, birthdate=birthdate, gender=gender)
        actor.insert()

        return jsonify({
            'success': True,
            'added': actor.short(),
        })
    except Exception:
        abort(500)


# Add a new movie
@routes.route('/movies', methods=['POST'])
@requires_auth('post:movies')
def create_movie(payload):
    body = request.get_json()
    title = body.get('title', None)
    release = body.get('release', None)  # 'YYYY-MM-DD'

    if title is None or release is None:
        abort(422)

    try:
        movie = Movie(title=title, release=release)
        movie.insert()

        return jsonify({
            'success': True,
            'added': movie.short(),
        })
    except Exception:
        abort(500)


# Edit an actor
@routes.route('/actors/<int:actor_id>', methods=['PATCH'])
@requires_auth('patch:actors')
def update_actor(payload, actor_id):
    body = request.get_json()
    name = body.get('name', None)
    birthdate = body.get('birthdate', None)  # 'YYYY-MM-DD'
    gender = body.get('gender', None)

    if name is None or birthdate is None or gender is None:
        abort(422)

    actor = Actor.query.get(actor_id)

    if not actor:
        return json.dumps({
            'success': False,
            'message': 'Actor not found to be edited'
        }), 404

    actor.name = name
    actor.birthdate = birthdate
    actor.gender = gender
    actor.update()

    return jsonify({
        'success': True,
        'updated': actor.short(),
    })


# Edit a movie
@routes.route('/movies/<int:movie_id>', methods=['PATCH'])
@requires_auth('patch:movies')
def update_movie(payload, movie_id):
    body = request.get_json()
    title = body.get('title', None)
    release = body.get('release', None)  # 'YYYY-MM-DD'

    if title is None or release is None:
        abort(422)

    movie = Movie.query.get(movie_id)

    if not movie:
        return json.dumps({
            'success': False,
            'message': 'Movie not found to be edited'
        }), 404

    movie.title = title
    movie.release = release
    movie.update()

    return jsonify({
        'success': True,
        'updated': movie.short(),
    })


@routes.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422


@routes.errorhandler(400)
def bad_request(error):
    return jsonify({
        "success": False,
        "error": 400,
        "message": "bad request"
    }), 400


@routes.errorhandler(401)
def unauthorized(error):
    return jsonify({
        "success": False,
        "error": 401,
        "message": "unauthorized"
    }), 401


@routes.errorhandler(403)
def forbidden(error):
    return jsonify({
        "success": False,
        "error": 403,
        "message": "forbidden"
    }), 403


@routes.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "resource not found"
    }), 404


@routes.errorhandler(405)
def not_allowed(error):
    return jsonify({
        "success": False,
        "error": 405,
        "message": "method not allowed"
    }), 405


@routes.errorhandler(500)
def server_error(error):
    return jsonify({
        "success": False,
        "error": 500,
        "message": "internal server error"
    }), 500


@routes.errorhandler(AuthError)
def auth_error(error):
    return jsonify({
        "success": False,
        "error": error.status_code,
        "message": error.error['description']
    }), error.status_code
