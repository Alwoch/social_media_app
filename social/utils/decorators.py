from functools import wraps

from flask import abort
from flask_jwt_extended import verify_jwt_in_request, current_user

from social.db import get_db
from .queries import get_post_by_id


def requires_account_owner():
    """verify a token is present and check if the token user is account owner"""
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()

            if current_user['id'] == kwargs['user_id']:
                return fn(*args, **kwargs)
            else:
                abort(403, description="unable to perform action")

        return decorator

    return wrapper


def requires_post_owner():
    """verify if the logged in user is the owner of a post"""
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()  # get the logged in user
            db = get_db()
            post_id = kwargs['post_id']

            # check if logged-in user is post author
            post = db.execute(get_post_by_id, (post_id,)).fetchone()

            if post is None:
                abort(404, description=f'post id {post_id} does not exist')

            if current_user['id'] == post['author_id']:
                return fn(*args, **kwargs)
            else:
                abort(403, description="unable to perform action")

        return decorator

    return wrapper
