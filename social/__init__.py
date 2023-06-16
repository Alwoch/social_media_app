import os
from datetime import timedelta

from flask import Flask
from flask_restful import Api, Resource
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.
bcrypt = Bcrypt()


def create_app(test_config=None):
    app = Flask(__name__)

    app.config['DATABASE'] = os.path.join(app.instance_path, 'social.sqlite')
    app.config.from_mapping(
        JWT_TOKEN_LOCATION=["cookies"],
        JWT_COOKIE_SECURE=False,  # TODO Change this to true for production
        JWT_SECRET_KEY=os.environ['JWT_SECRET_KEY'],
        JWT_ACCESS_TOKEN_EXPIRES=timedelta(hours=24)
    )
    jwt = JWTManager(app)

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

    # verify the jwt id in the database
    from .utils.queries import find_by_id
    from .db import get_db
    from .schemas.user import UserSchema

    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
        identity = jwt_data["sub"]['id']
        db = get_db()
        user = db.execute(find_by_id, (identity,)).fetchone()
        return UserSchema().dump(user) if user else None

    # error for when loading the user identity fails eg deleted from the database
    @jwt.user_lookup_error_loader
    def user_lookup_error_callback(_jwt_header, jwt_data):
        return {'msg': 'user not found'}, 404

    # return custom message when not logged in
    @jwt.unauthorized_loader
    def unauthorized_callback(reason):
        return {'msg': 'please log in to access this route'}, 401

    class Hello(Resource):
        def get(self):
            return {'message': 'hello world'}

    # routes
    from .resources.auth import Signup, Login, Logout
    from .resources.user import UsersList, User, LoggedInUser
    from .resources.post import Post

    api.add_resource(Hello, '/')
    api.add_resource(Signup, '/auth/signup')
    api.add_resource(Login, '/auth/login')
    api.add_resource(Logout, '/auth/logout')
    api.add_resource(UsersList, '/users')
    api.add_resource(LoggedInUser, '/users/me')
    api.add_resource(User, '/users/<str:user_id>')
    api.add_resource(Post, '/posts')

    return app
