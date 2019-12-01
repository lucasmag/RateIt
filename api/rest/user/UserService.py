from api.rest.user import UserRepository as repository
from api.utils import jsonify
from sanic import response
import asyncpg


async def db_query(request, func):
    async with request.app.config['pool'].acquire() as conn:
        resp = await conn.fetch(func)
        return response.json(jsonify.make_json(resp), status=200)


async def get_user_by_id(request, user_id):
    return db_query(request, repository.get_user_by_id(user_id))


async def get_followers_by_user_id(request, user_id):
    return db_query(request, repository.get_followers_by_user_id(user_id))


async def follow_user(request, follower_id, followed_id):
    return await db_query(request, repository.follow_user(follower_id, followed_id))


async def unfollow_user(request, follower_id, followed_id):
    return await db_query(request, repository.unfollow_user(follower_id, followed_id))


async def create_user(request):
    try:
        return await db_query(request, repository.new_user(request.json))

    except asyncpg.UniqueViolationError:
        return response.text('Já existe um perfil com este nome de usuário cadastrado!')
