import api.modules.user.repository as r
from sanic import response, Blueprint
from others import jsonify as j

users = Blueprint('users', url_prefix='/usuarios')


def pool(request):
    return request.app.config['pool']


@users.route("/todos", methods=['GET'])
async def get_users(request):
    async with pool(request).acquire() as conn:
        resp = await conn.fetch(r.get_users())
        return response.json(j.jsonify(resp), status=200)


@users.route("/<id>", methods=['GET'])
async def get_user_by_id(request, id):
    async with pool(request).acquire() as conn:
        resp = await conn.fetch(r.get_user_by_id(id))
        return response.json(j.jsonify(resp), status=200)
