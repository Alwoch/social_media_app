import uuid

from flask import abort, request

from flask_restful import Resource
from flask_jwt_extended import jwt_required, current_user
from marshmallow import ValidationError

from social.db import get_db
from social.schemas.post import PostSchema
from social.utils.queries import create_post, get_posts_by_author_id, update_post, delete_post,get_feed
from social.utils.decorators import requires_post_owner


class PostList(Resource):
    """create post"""
    @jwt_required()
    def post(self):
        db = get_db()
        json_data = request.get_json()

        # validate and deserialize
        try:
            data = PostSchema().load(json_data)
        except ValidationError as e:
            return e.messages, 400

        new_post_id = uuid.uuid4()
        db.execute(create_post,
                   (str(new_post_id), data['title'], data['content'], current_user['id']))
        db.commit()

        return {'msg': 'post successfully created'}, 201

    """user gets own posts with pagination"""
    @jwt_required()
    def get(self):
        page_number = request.args.get('page', default=1, type=int)
        limit = request.args.get('posts', default=10, type=int)
        offset = (page_number-1)*limit

        db = get_db()

        rows = db.execute(get_posts_by_author_id,
                          (current_user['id'], limit, offset)).fetchall()

        result = [dict(row) for row in rows]
        posts = PostSchema().dump(result, many=True)

        return {'count': len(posts), 'posts': posts}, 200


class Post(Resource):
    """update a post"""
    @requires_post_owner()
    def patch(self, post_id):
        db = get_db()
        json_data = request.get_json()

        # validate and deserialize
        try:
            data = PostSchema().load(json_data, partial=True)
        except ValidationError as e:
            return e.messages, 400

        update_post_query = update_post
        update_post_params = []

        #check for non empty fields and add them to the post_params
        for field in data:
            if data[field] is not None:
                update_post_query += f' {field} =?,'
                update_post_params.append(data[field])

        # update for parameters provided
        if len(update_post_params) > 0:
            update_post_query = update_post_query[:-1]  # remove trailing comma
            update_post_query += f' WHERE id=?'
            update_post_params.append(post_id)

            # save updated data
            db.execute(update_post_query, update_post_params)
            db.commit()

            return {'msg': 'post successfully updated'}, 200
        else:
            return {'msg': 'no new changes provided'}

    """logged in user deletes their post"""
    @requires_post_owner()
    def delete(self, post_id):
        db = get_db()

        db.execute(delete_post, (post_id,))
        db.commit()

        return {'msg': 'post has been successfully deleted'}, 200


class PostsFeed(Resource):
    """generate a list of posts to whoch the logged in user is invited"""
    @jwt_required()
    def get(self):
        page_number = request.args.get('page', default=1, type=int)
        limit = request.args.get('posts', default=10, type=int)
        offset = (page_number-1)*limit

        db = get_db()

        rows = db.execute(get_feed,
                          (current_user['id'], limit, offset)).fetchall()

        result = [dict(row) for row in rows]
        posts = PostSchema().dump(result, many=True)

        return {'count': len(posts), 'posts': posts}, 200