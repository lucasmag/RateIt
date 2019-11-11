from sanic import Blueprint
from api.rest.user import UserService as service

users = Blueprint('users', url_prefix='/usuarios')


def pool(request):
    return request.app.config['pool']


@users.route("/todos", methods=['GET'])
async def get_users(request):
    return await service.get_all_users(request)


@users.route("/novo", methods=['POST'])
async def create_user(request):
    return await service.create_user(request)


@users.route("/<user_id>", methods=['GET'])
async def get_user_by_id(request, user_id):
    return service.get_user_by_id(request, user_id)


@users.route("/<user_id>/seguidores", methods=['GET'])
async def get_followers_by_user_id(request, user_id):
    return service.get_followers_by_user_id(request, user_id)


@users.route("/<followed_id>/seguir", methods=['POST'])
async def follow_user(request, followed_id):
    return await service.follow_user(request, request.json.get('follower_id'), followed_id)


@users.route("/<followed_id>/deixar-de-seguir", methods=['DELETE'])
async def unfollow_user(request, followed_id):
    return await service.unfollow_user(request, request.json.get('follower_id'), followed_id)