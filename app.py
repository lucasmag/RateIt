from asyncpg import create_pool, connect
from sanic import Sanic, response
from sanic_auth import Auth
from sanic_cors import CORS
from api.rest.user.UserVO import User
from api import api
import os


app = Sanic(__name__)
app.config.AUTH_LOGIN_ENDPOINT = 'login'
app.blueprint(api)
auth = Auth(app)
CORS(app)

DATABASE_URL = os.environ['DATABASE_URL']


session = {}
@app.middleware('request')
async def add_session(request):
    request['session'] = session


@app.listener('before_server_start')
async def register_db(app, loop):

    # Create a database connection pool
    app.config['pool'] = await create_pool(
        dsn=DATABASE_URL,
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
    conn = await connect(DATABASE_URL, ssl=True)
    with open("api/schema.sql", "r") as sql:
        await conn.execute(sql.read())


@app.listener('after_server_stop')
async def close_connection(app, loop):
    pool = app.config['pool']
    async with pool.acquire() as conn:
        await conn.close()

LOGIN_FORM = '''
<h2>Please sign in, you can try:</h2>
<dl>
<dt>Username</dt> <dd>demo</dd>
<dt>Password</dt> <dd>1234</dd>
</dl>
<p>{}</p>
<form action="" method="POST">
  <input class="username" id="name" name="username"
    placeholder="username" type="text" value=""><br>
  <input class="password" id="password" name="password"
    placeholder="password" type="password" value=""><br>
  <input id="submit" name="submit" type="submit" value="Sign In">
</form>
'''


async def db_query(request, func):
    async with request.app.config['pool'].acquire() as conn:
        resp = await conn.fetchrow(func)
        return dict(resp)


@app.route('/login', methods=['GET', 'POST'])
async def login(request):
    message = ''
    if request.method == 'POST':

        username = request.json.get('username')
        password = request.json.get('password')

        # fetch user from database
        user = await db_query(request, "select * from public.user u where u.username = '{}'".format(username))
        if user and user['password'] == password:
            user = User(user['id'], user['name'])
            auth.login_user(request, user)
            return response.redirect('/')
    return response.html(LOGIN_FORM.format(message))


@app.route('/logout')
@auth.login_required
async def logout(request):
    auth.logout_user(request)
    return response.redirect('/login')


@app.route('/')
@auth.login_required(user_keyword='user')
async def profile(request, user):
    content = '<a href="/logout">Logout</a><p>Welcome, %s</p>' % user.name
    return response.html(content)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
