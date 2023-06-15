from flask import request
from flask_restful import Resource
from marshmallow import ValidationError

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
            return {"message": "username already exists"}, 409

        # save the user
        db.execute(create_user, (
            data['username'],
            data['phone_number'],
            bcrypt.generate_password_hash(data['password']).decode('utf-8')
        ))
        db.commit()

        return {"message": "user successfully created"}, 201

class Login(Resource):
    def post(self):
        db=get_db
        json_data=request.get_json()

        try:
            data = UserSchema().load(json_data)
        except ValidationError as err:
            return err.messages, 400
