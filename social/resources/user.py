from flask import request

from flask_restful import Resource
from flask_jwt_extended import jwt_required, current_user

from social.db import get_db
from social.utils.queries import fetch_all_users
from social.schemas.user import UserSchema
from social.utils.decorators import requires_account_owner


class UsersList(Resource):
    """list all users with pagination"""
    def get(self):
        page_number = request.args.get('page', default=1, type=int)
        limit = request.args.get('users', default=10, type=int)
        offset = (page_number-1)*limit

        db = get_db()
        user_schema = UserSchema()

        rows = db.execute(fetch_all_users, (limit, offset)).fetchall()
        result = [dict(row) for row in rows]
        users = user_schema.dump(result, many=True)

        return {'count': len(users), 'users': users}, 200

# TODO -Delete route
# TODO -update route
# TODO -paginate users


class LoggedInUser(Resource):
    """get the current logged in user"""
    @jwt_required()
    def get(self):
        return current_user


class User(Resource):
    @requires_account_owner()
    def get(self, user_id):
        return {'msg': 'safe'}
