from flask import request

from flask_restful import Resource
from marshmallow import ValidationError
from flask_jwt_extended import jwt_required, current_user

from social.db import get_db
from social.utils.queries import fetch_all_users, update_user, delete_user
from social.schemas.user import UserSchema, UpdateUserSchema
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


class LoggedInUser(Resource):
    """get the current logged in user"""
    @jwt_required()
    def get(self):
        return current_user


class User(Resource):
    """user updates their account"""
    @requires_account_owner()
    def patch(self, user_id):
        db = get_db()
        json_data = request.get_json()

        # validate and deserialize
        try:
            data = UpdateUserSchema().load(json_data, partial=True)
        except ValidationError as e:
            return e.messages, 400

        update_user_query = update_user
        update_user_params = []

        for field in data:
            if data[field] is not None:
                update_user_query += f' {field} =?,'
                update_user_params.append(data[field])

        # update for parameters provided
        if len(update_user_params) > 0:
            update_user_query = update_user_query[:-1]  # remove trailing comma
            update_user_query += f' WHERE id=?'
            update_user_params.append(user_id)

            # save updated data
            db.execute(update_user_query, update_user_params)
            db.commit()

            return {'msg': 'user successfully updated'}, 200
        else:
            return {'msg': 'no new changes provided'}

    """user deletes their account"""
    @requires_account_owner()
    def delete(self, user_id):
        db = get_db()

        db.execute(delete_user, (user_id,))
        db.commit()

        return {'msg': 'user has been successfully deleted'}, 200
