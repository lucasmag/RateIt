from sanic import Blueprint
from .rest.user.UserResource import users
from .rest.movie.MovieResource import movies

api = Blueprint.group(users, movies, url_prefix='/api')
