from flask import request
from flask_restful import Resource
from marshmallow import ValidationError

from social.schemas.user import UserSchema
from social.models.user import User
from social import bcrypt


class Signup(Resource):
    def post(self):
        json_data = request.get_json()

        # validate and deserialise
        try:
            data = UserSchema().load(json_data)
        except ValidationError as err:
            return err.messages, 400

        if User.find_by_username(data["username"]):
            return {"message": "username already exists"}, 409

        username, phone_number = data["username"], data["phone_number"]
        password = bcrypt.generate_password_hash(data["password"])

        user = User(username, phone_number, password)
        user.save_to_db()
        return {"message": "user successfully created"}, 201
