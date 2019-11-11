from sanic_auth import Auth
from sanic import Sanic, response

app = Sanic(__name__)
app.config.AUTH_LOGIN_ENDPOINT = 'login'


@app.middleware('request')
async def add_session_to_request(request):
    #setup session

auth = Auth(app)

@app.route('/login', methods=['GET', 'POST'])
async def login(request):
    message = ''
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        # fetch user from database
        user = some_datastore.get(name=username)
        if user and user.check_password(password):
            auth.login_user(request, user)
            return response.redirect('/profile')
    return response.html(HTML_LOGIN_FORM)


@app.route('/logout')
@auth.login_required
async def logout(request):
    auth.logout_user(request)
    return response.redirect('/login')


@app.route('/profile')
@auth.login_required(user_keyword='user')
async def profile(request, user):
    return response.json({'user': user})