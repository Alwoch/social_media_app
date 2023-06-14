import os

from flask import Flask
from flask_restful import Api, Resource
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.
bcrypt = Bcrypt()


def create_app(test_config=None):
    app = Flask(__name__)
    app.config['DATABASE_URI'] = os.environ['DATABASE_URI']

    app.config.from_mapping(
        DATABASE=os.path.join(app.instance_path, 'social.sqlite'),
    )

    if test_config is not None:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # database
    from . import db
    db.init_app(app)

    api = Api(app, catch_all_404s=True)

    class Hello(Resource):
        def get(self):
            return {'message': 'hello world'}

    # routes
    from .resources.auth import Signup

    api.add_resource(Hello, '/')
    api.add_resource(Signup, '/auth/signup')

    return app

