from asyncpg import create_pool, connect
from sanic import Sanic
from api import api
import os


app = Sanic(__name__)
app.blueprint(api)


@app.listener('before_server_start')
async def register_db(app, loop):

    # Create a database connection pool
    conn = "postgres://{user}:{password}@{host}:{port}/{database}".format(
        user='postgres', password='postgres', host='localhost',
        port=5432, database='postgres'
    )

    app.config['pool'] = await create_pool(
        dsn=conn,
        # in bytes
        min_size=10,
        # in bytes
        max_size=10,
        # maximum query
        max_queries=50000,
        # maximum idle times
        max_inactive_connection_lifetime=300,
        loop=loop
    )

    # Initialize database
    conn = await connect(host="localhost", port=5432, user="postgres", password="postgres", database="postgres")
    with open("api/schema.sql", "r") as sql:
        await conn.execute(sql.read())


@app.listener('after_server_stop')
async def close_connection(app, loop):
    pool = app.config['pool']
    async with pool.acquire() as conn:
        await conn.close()


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
