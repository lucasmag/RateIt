from sanic import Blueprint
from .modules.user.user import users

api = Blueprint.group(users, url_prefix='/api')
