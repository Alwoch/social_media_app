from functools import wraps

from flask import abort
from flask_jwt_extended import verify_jwt_in_request, current_user


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
