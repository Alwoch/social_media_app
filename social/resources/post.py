from flask import abort, request

from flask_restful import Resource
from flask_jwt_extended import jwt_required, current_user
from marshmallow import ValidationError

from social.db import get_db
from social.schemas.post import PostSchema
from social.utils.queries import create_post


class Post(Resource):
    """create post"""
    @jwt_required()
    def post(self):
        db = get_db()
        json_data = request.get_json()
        print(json_data)

        # validate and serialize
        try:
            data = PostSchema().load(json_data)
            print(data)
        except ValidationError as e:
            return e.messages, 400

        post=db.execute(create_post,
                   (data['title'], data['content'], current_user['id']))

        return PostSchema.dump(post),201
