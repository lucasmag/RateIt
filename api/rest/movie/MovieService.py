import requests
import api.utils.url_maker as url


async def get_popular():
    print(url.make('movie', first_id='popular'))
    response = requests.get(url.make('movie', first_id='popular'))
    return response.json()


async def get_top_rated():
    response = requests.get(url.make('movie', first_id='top_rated'))
    return response.json()


async def get_recommendations_by_a_movie(movie_id):
    response = requests.get(url.make('movie', first_id=movie_id, path='recommendations'))
    return response.json()
