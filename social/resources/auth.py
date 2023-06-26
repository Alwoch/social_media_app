import uuid

from flask import request, jsonify, abort
from flask_restful import Resource
from marshmallow import ValidationError
from flask_jwt_extended import create_access_token, set_access_cookies, unset_jwt_cookies,jwt_required

from social.schemas.user import UserSchema
from social import bcrypt
from social.db import get_db
from social.utils import find_user_by_username
from social.utils.queries import find_by_username, create_user


class Signup(Resource):
    # TODO: ADD DOCUSTRINGS FOR ALL CLASSES AND METHODS. DOCUMENTATION IS IMPORTANT
    # TODO: WHAT THE CLASS DOES, WHAT THE METHOD DOES, WHAT THE ENDPOINT DOES
    # TODO: ADD VALIDATION TO ALL ENDPOINTS
    # TODO: ADD DOCSTRING TO ALL ENDPOINTS
    # TODO: ADD PARAMETER TYPES TO ALL ENDPOINTS DOCUMENTATION
    # TODO: ADD RETURN TYPES TO ALL ENDPOINTS DOCUMENTATION
    """creates a new user"""
    def post(self):
        db = get_db()
        json_data = request.get_json()

        # validate and deserialise
        try:
            data = UserSchema().load(json_data)
        except ValidationError as err:
            return err.messages, 400

        #check for existing username
        existing_user = find_user_by_username(data['username'])

        if existing_user is not None:
            abort(400, description="username already exists") # TODO: WHY NOT RETURN EXCEPTION RATHER THAN ABORT

        # save the user
        user_id = uuid.uuid4()
        db.execute(create_user, (
            str(user_id),
            data['username'],
            data['phone_number'],
            bcrypt.generate_password_hash(data['password']).decode('utf-8')
        ))
        db.commit()

        return {"message": "user successfully created"}, 201


class Login(Resource):
    # TODO: ADD DOCUSTRINGS FOR ALL CLASSES AND METHODS. DOCUMENTATION IS IMPORTANT
    # TODO: WHAT THE CLASS DOES, WHAT THE METHOD DOES, WHAT THE ENDPOINT DOES
    # TODO: ADD VALIDATION TO ALL ENDPOINTS
    # TODO: ADD DOCSTRING TO ALL ENDPOINTS
    # TODO: ADD PARAMETER TYPES TO ALL ENDPOINTS DOCUMENTATION
    # TODO: ADD RETURN TYPES TO ALL ENDPOINTS DOCUMENTATION

    """Login and attach cookies to response"""

    def post(self):
        json_data = request.get_json()
        user_schema = UserSchema()

        try:
            data = user_schema.load(json_data, partial=True)
        except ValidationError as err:
            return err.messages, 400

        #check for the user in the database
        user = find_user_by_username(data['username'])

        if user is None:
            abort(404, description="user not found")
        elif not bcrypt.check_password_hash(user['password'], data['password']):
            abort(400, description="invalid login credentials")

        #generate access token and save it in cookies
        serialised_user = UserSchema().dump(user)
        response = jsonify({'message': 'you are logged in'})
        access_token = create_access_token(identity=serialised_user)
        set_access_cookies(response, access_token)

        return response


class Logout(Resource):
    # TODO: ADD DOCUSTRINGS FOR ALL CLASSES AND METHODS. DOCUMENTATION IS IMPORTANT
    # TODO: WHAT THE CLASS DOES, WHAT THE METHOD DOES, WHAT THE ENDPOINT DOES
    # TODO: ADD VALIDATION TO ALL ENDPOINTS
    # TODO: ADD DOCSTRING TO ALL ENDPOINTS
    # TODO: ADD PARAMETER TYPES TO ALL ENDPOINTS DOCUMENTATION
    # TODO: ADD RETURN TYPES TO ALL ENDPOINTS DOCUMENTATION
    
    """log out and remove token from cooke"""
    @jwt_required()
    def get(self):
        response = jsonify({"message": "logged out successfully"})
        unset_jwt_cookies(response)
        return response
