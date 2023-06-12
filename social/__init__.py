import os

from flask import Flask
from flask_restful import Api, Resource
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_mapping(
        SQLALCHEMY_DATABASE_URI=os.environ.get('DATABASE_URI'),
        SQLALCHEMY_TRACK_MODIFICATIONS=False
    )

    if test_config is None:
        # load the instance config when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config
        app.config.from_mapping(test_config)

    # create the instance folder
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    api = Api(app)

    class Hello(Resource):
        def get(self):
            return {'message': 'hello world'}

    # routes
    api.add_resource(Hello, '/')

    # database
    from . import db
    db.create_tables(app)

    return app
