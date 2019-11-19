from sanic_auth import Auth
from sanic import Sanic, response
from api.utils import jsonify

app = Sanic(__name__)
app.config.AUTH_LOGIN_ENDPOINT = 'login'


@app.middleware('request')
async def add_session_to_request(request):


auth = Auth(app)


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
        resp = await conn.fetch(func)
        return jsonify.make_json(resp)



@app.route('/login', methods=['GET', 'POST'])
async def login(request):
    message = ''
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        # fetch user from database
        user = await db_query(request, 'select u from public.user u where u.username = {}'.format(username))
        if user and user.get('password') == password:
            auth.login_user(request, user)
            return response.redirect('/profile')
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