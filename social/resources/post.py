import uuid

from flask import abort, request

from flask_restful import Resource
from flask_jwt_extended import jwt_required, current_user
from marshmallow import ValidationError

from social.db import get_db
from social.schemas.post import PostSchema
from social.utils.queries import create_post, get_posts_by_author_id


class Post(Resource):
    """create post"""
    @jwt_required()
    def post(self):
        db = get_db()
        json_data = request.get_json()

        # validate and serialize
        try:
            data = PostSchema().load(json_data)
        except ValidationError as e:
            return e.messages, 400

        new_post_id=uuid.uuid4()
        db.execute(create_post,
                   (str(new_post_id),data['title'], data['content'], current_user['id']))
        db.commit()

        return {'msg': 'post successfully created'}, 201

    """user gets own posts"""
    # TODO add pagination to this
    @jwt_required()
    def get(self):
        db = get_db()

        rows = db.execute(get_posts_by_author_id,
                          (current_user['id'],)).fetchall()

        result = [dict(row) for row in rows]
        posts = PostSchema().dump(result, many=True)

        return posts, 200
