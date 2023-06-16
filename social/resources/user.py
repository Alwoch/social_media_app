from flask_restful import Resource
from flask_jwt_extended import jwt_required, current_user

from social.db import get_db
from social.utils.queries import fetch_all_users
from social.schemas.user import UserSchema
from social.utils.decorators import requires_account_owner


# TODO: refactor get all users to include pagination

class UsersList(Resource):
    def get(self):
        db = get_db()
        user_schema = UserSchema()

        rows = db.execute(fetch_all_users).fetchall()
        result = [dict(row) for row in rows]
        users = user_schema.dump(result, many=True)

        return users, 200

#TODO -Delete route
#TODO -update route
#TODO -paginate users
class User(Resource):
    """get the current logged in user"""
    @jwt_required()
    def get(self):
        return current_user
    
    @requires_account_owner()
    def get(self,user_id):
        return {'msg':'safe'}
