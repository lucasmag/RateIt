import requests
import api.utils.constants as c
import api.utils.url_maker as url


async def get_popular():
    response = requests.get(url.make(c.TMDB_BASE_URL, 'movie', first_id='popular'))
    return response.json()


async def get_top_rated():
    response = requests.get(url.make(c.TMDB_BASE_URL, 'movie', first_id='top_rated'))
    return response.json()


async def get_recommendations_by_a_movie(movie_id):
    response = requests.get(url.make(c.TMDB_BASE_URL, 'movie', first_id=movie_id, path='recommendations'))
    return response.json()


async def get_poster(movie_id):
    movie = await get_movie_by_id(movie_id)
    return c.IMAGE + '/' + movie['backdrop_path']


async def get_movie_by_id(movie_id):
    response = requests.get(url.make(c.TMDB_BASE_URL, 'movie', first_id=movie_id))
    return response.json()
