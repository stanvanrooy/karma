import flask
import auth
from functools import wraps

def require_login():
    def _require_login(f):
        @wraps(f)
        def __require_login(*args, **kwargs):
            authorization = flask.request.headers.get('Authorization')
            if authorization is None:
                return "Unauthorized", 401

            type, token = authorization.split(' ')
            if type != 'Bearer':
                return "Unauthorized", 401

            user = auth.validate_access_token(token)
            if user is None:
                return "Unauthorized", 401

            flask.session['user'] = user

            return f(*args, **kwargs)
        return __require_login
    return _require_login

