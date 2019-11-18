from sanic_cors import CORS, cross_origin
from sanic import Sanic
from api import api
import os


app = Sanic(__name__)
CORS(app)
app.blueprint(api)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
