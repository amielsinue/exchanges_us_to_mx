import os

from flask import Flask
from flask_restful import Api
from flask_cors import CORS

from .auth.resource import Login, Register
from .exchanges.resource import Exchanges
from app.data import db, cache


def create_app():

    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    CORS(app, resources={r"/*": {"origins": "*"}})

    app.config.from_object('config')
    # app.config.from_pyfile('./config.py', silent=True)

    db.init_app(app)
    cache.init_app(app, app.config)

    api = Api(app)

    api.add_resource(Login, '/auth/login')
    api.add_resource(Register, '/auth/register')
    api.add_resource(Exchanges, '/exchanges')

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/')
    def hello_world():
        return 'Dollar Peso Exchange API 1.0'

    return app