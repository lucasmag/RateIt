from asyncpg import create_pool, connect
from sanic import Sanic
from api import api
import os


app = Sanic(__name__)
app.blueprint(api)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
