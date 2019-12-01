import asyncpg

from api.rest.movie import MovieRepository as repository
import api.utils.url_maker as url
import api.utils.constants as c
from api.utils import jsonify
from sanic import response
import requests


async def db_query(request, func):
    async with request.app.config['pool'].acquire() as conn:
        resp = await conn.fetch(func)
        return response.json(jsonify.make_json(resp), status=200)


async def synchronize_movies(movies):
    try:
        return await db_query(movies, repository.sync_movie(movies.json()['results']))

    except asyncpg.UniqueViolationError:
        vote_count, vote_average = await db_query(movies, repository.sync_movie(movies.json()['results']))
        for movie in movies.json(['results']):
            movie['vote_count']
            movie['vote_average']


async def get_popular():
    popular = requests.get(url.make(c.TMDB_BASE_URL, 'movie', first_id='popular'))
    return await synchronize_movies(popular)


async def get_top_rated():
    resp = requests.get(url.make(c.TMDB_BASE_URL, 'movie', first_id='top_rated'))
    return resp.json()


async def get_recommendations_by_a_movie(movie_id):
    resp = requests.get(url.make(c.TMDB_BASE_URL, 'movie', first_id=movie_id, path='recommendations'))
    return resp.json()


async def get_poster(movie_id):
    movie = await get_movie_by_id(movie_id)
    return c.IMAGE + '/' + movie['backdrop_path']


async def get_movie_by_id(movie_id):
    resp = requests.get(url.make(c.TMDB_BASE_URL, 'movie', first_id=movie_id))
    return resp.json()


async def rate_movie(request, movie_id):
    return await db_query(request, repository.rate_movie(request.json.get('user_id'),
                                                         movie_id, request.json.get('rating')))
