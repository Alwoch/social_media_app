from social.db import get_db
from .queries import find_by_username


def find_user_by_username(username):
    """find a user by their username"""
    return get_db().execute(find_by_username, (username,)).fetchone()
