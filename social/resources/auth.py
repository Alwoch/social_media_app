from flask import request, jsonify, abort
from flask_restful import Resource
from marshmallow import ValidationError
from flask_jwt_extended import create_access_token, set_access_cookies, unset_jwt_cookies

from social.schemas.user import UserSchema
from social import bcrypt
from social.db import get_db
from social.utils.queries import find_by_username, create_user


class Signup(Resource):
    def post(self):
        db = get_db()
        json_data = request.get_json()

        # validate and deserialise
        try:
            data = UserSchema().load(json_data)
        except ValidationError as err:
            return err.messages, 400

        existing_user = db.execute(
            find_by_username, (data["username"],)).fetchone()

        if existing_user is not None:
            abort(400, description="user already exists")

        # save the user
        db.execute(create_user, (
            data['username'],
            data['phone_number'],
            bcrypt.generate_password_hash(data['password']).decode('utf-8')
        ))
        db.commit()

        return {"message": "user successfully created"}, 201


class Login(Resource):
    """Login and attach cookies to response"""

    def post(self):
        db = get_db()
        json_data = request.get_json()
        user_schema = UserSchema()

        try:
            data = user_schema.load(json_data, partial=True)
        except ValidationError as err:
            return err.messages, 400

        user = db.execute(find_by_username, (data['username'],)).fetchone()

        if user is None:
            abort(404, description="user not found")
        elif not bcrypt.check_password_hash(user['password'], data['password']):
            abort(400, description="invalid login credentials")

        serialised_user=UserSchema().dump(user)
        response = jsonify({'message': 'you are logged in'})
        access_token = create_access_token(identity=serialised_user)
        set_access_cookies(response, access_token)

        return response


class Logout(Resource):
    """log out and remove token from cooke"""

    def get(self):
        response = jsonify({"message": "logged out successfully"})
        unset_jwt_cookies(response)
        return response
