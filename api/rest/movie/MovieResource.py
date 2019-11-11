from sanic import response, Blueprint

from api.rest.movie import MovieService as service

movies = Blueprint('movie', url_prefix='/filmes')


@movies.route("/populares", methods=['GET'])
async def get_popular(request):
    resp = await service.get_popular()
    return response.json(resp, status=200)


@movies.route("/mais-votados", methods=['GET'])
async def get_top_rated(request):
    resp = await service.get_top_rated()
    return response.json(resp, status=200)


@movies.route("/<id>/recomendados", methods=['GET'])
async def get_recommendations(request, id):
    resp = await service.get_recommendations_by_a_movie(id)
    return response.json(resp, status=200)




