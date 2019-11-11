from api.rest.user import UserRepository as repository
from api.utils import jsonify
from sanic import response


def pool(request):
    return request.app.config['pool']


async def make_request(request, func):
    async with pool(request).acquire() as conn:
        resp = await conn.fetch(func)
        return response.json(jsonify.make_json(resp), status=200)


############


async def get_all_users(request):
    return await make_request(request, repository.get_users())


async def get_user_by_id(request, user_id):
    return make_request(request, repository.get_user_by_id(user_id))


async def get_followers_by_user_id(request, user_id):
    return make_request(request, repository.get_followers_by_user_id(user_id))


async def follow_user(request, follower_id, followed_id):
    return await make_request(request, repository.follow_user(follower_id, followed_id))


async def unfollow_user(request, follower_id, followed_id):
    return await make_request(request, repository.unfollow_user(follower_id, followed_id))


async def create_user(request):
    return await make_request(request, repository.new_user(request.json))
