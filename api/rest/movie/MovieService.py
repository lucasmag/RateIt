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


async def db(request, func):
    async with request.app.config['pool'].acquire() as conn:
        return await conn.fetch(func)


async def synchronize_movies(request, movie):
    try:
        await db_query(request, repository.new_movie(movie['id']))
        votes = await db(request, repository.sync_movie(movie['id']))
        return await subs_votes(movie, votes)

    except asyncpg.UniqueViolationError:
        votes = await db(request, repository.sync_movie(movie['id']))
        return await subs_votes(movie, votes)


async def subs_votes(movie, votes):
    vote_count, vote_average = votes[0]['vote_count'], votes[0]['vote_average']
    movie['vote_count'] = vote_count
    movie['vote_average'] = vote_average
    print(type(movie))
    return response.json(movie, status=200)


async def get_popular():
    resp = requests.get(url.make(c.TMDB_BASE_URL, 'movie', first_id='popular'))
    return resp.json()


async def get_top_rated():
    resp = requests.get(url.make(c.TMDB_BASE_URL, 'movie', first_id='top_rated'))
    return resp.json()


async def get_recommendations_by_a_movie(movie_id):
    resp = requests.get(url.make(c.TMDB_BASE_URL, 'movie', first_id=movie_id, path='recommendations'))
    return resp.json()


async def get_poster(movie_id):
    movie = await get_movie_by_id(movie_id)
    return c.IMAGE + '/' + movie['backdrop_path']


async def get_movie_by_id(request, movie_id):
    resp = requests.get(url.make(c.TMDB_BASE_URL, 'movie', first_id=movie_id))
    new_resp = await synchronize_movies(request, resp.json())
    return new_resp


async def rate_movie(request, movie_id):
    return await db_query(request, repository.rate_movie(request.json.get('user_id'),
                                                         movie_id, request.json.get('rating')))
