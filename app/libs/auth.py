from datetime import datetime

from flask import request
from flask_restful import abort
from functools import wraps

from app.users.model import User
from app.data import cache


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization', '').replace('Token ', '')
        if not token:
            abort(401, message="Authentication required")
        user = User.query.filter_by(api_token=token).first()
        if not user:
            abort(401, message="Invalid Token")
        now = datetime.now()
        diff = now - user.api_token_created_at
        auth_ok = diff.days < 1
        if not auth_ok:
            return abort(401, message="Token Expired")

        ## check limit
        cache_key = '{}-requests'.format(user.id)
        count = cache.get(cache_key)
        if not count:
            count = 0

        count = count + 1
        if count >= user.max_requests_count:
            return abort(401, message="Reached requests limit, please try again later")

        cache.set(cache_key, count, timeout=60)
        return f(*args, **kwargs)
    return decorated
