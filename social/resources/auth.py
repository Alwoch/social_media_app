from flask import request
from flask_restful import Resource
from marshmallow import ValidationError

from social.schemas.user import UserSchema
from social import bcrypt
from social.db import get_db


class Signup(Resource):
    def post(self):
        db=get_db()
        json_data = request.get_json()

        # validate and deserialise
        try:
            data = UserSchema().load(json_data)
        except ValidationError as err:
            return err.messages, 400

        #TODO finalise refactoring this function

        # if User.find_by_username(data["username"]):
        #     return {"message": "username already exists"}, 409

        username, phone_number = data["username"], data["phone_number"]
        password = bcrypt.generate_password_hash(data["password"])

        query='INSERT INTO users (username,phone_number,password) VALUES (?,?,?)'
        db.execute(query,(username,phone_number,password))
       
        return {"message": "user successfully created"}, 201
