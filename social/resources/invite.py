import uuid

from flask import abort

from flask_restful import Resource
from flask_jwt_extended import current_user

from social.utils.decorators import requires_post_owner
from social.utils.queries import get_invite, create_invite, revoke_invite
from social.utils import find_user_by_username
from social.db import get_db


class Invite(Resource):
    """invite a user"""
    @requires_post_owner()
    def post(self, post_id, user_name):
        db = get_db()

        # check if user being invited exists
        user = find_user_by_username(user_name)

        if user is None:
            abort(404, description='user not found')

        # check the user is already invited to the post
        existing_invite = db.execute(
            get_invite, (user_name, post_id,)).fetchone()

        if existing_invite is not None:
            abort(
                409, description=f'{user_name} is already invited to this post')

        invite_id = uuid.uuid4()
        db.execute(create_invite, (str(invite_id), post_id,
                   current_user['id'], user_name))
        db.commit()

        return {'msg': f'{user_name} has been invited to this post'}, 201

    """revoke invite"""
    @requires_post_owner()
    def delete(self, post_id, user_name):
        db = get_db()
        result = db.execute(revoke_invite, (user_name, post_id))

        if result.rowcount > 0:
            db.commit()
            return {'msg': f'{user_name} has been uninvited to this post'}
        else:
            return {'msg': 'invitation not found'}, 404
