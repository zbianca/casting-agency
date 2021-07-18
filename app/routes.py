import os
from flask import Flask
from app import app
from app.models import Movie, Actor


# TODO: Render README
@app.route('/')
def get_intro():
    return "Hello!!!"
