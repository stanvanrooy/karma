import jwt
import time
from typing import Optional
import logging

ACCESS_TOKEN_EXP = 30
REFRESH_TOKEN_EXP = 60 * 24


def generate_access_token(username: str) -> str:
    return _encode(username, 'access_token', ACCESS_TOKEN_EXP)


def generate_refresh_token(username: str) -> str:
    return _encode(username, 'refresh_token', REFRESH_TOKEN_EXP)


def validate_access_token(token: str) -> Optional[str]:
    return _validate(token, 'access_token')


def validate_refresh_token(token: str) -> Optional[str]:
    return _validate(token, 'refresh_token')


def _validate(token: str, t: str) -> Optional[str]:
    try:
        data = jwt.decode(token, _get_secret(), algorithms=['HS256'])
        if data['type'] != t:
            logging.info('invalid token - incorrect type')
            return None
        if data['exp'] < str(int(time.time())):
            logging.info('invalid token - expired')
            return None
        return data['sub']
    except jwt.ExpiredSignatureError:
        logging.info('invalid token - expired')
        return None
    except jwt.InvalidTokenError:
        logging.info('invalid token - invalid')
        return None


def _encode(user: str, t: str, exp: int) -> str:
    data = {
        'sub': user,
        'type': t,
        'exp': _get_exp(exp),
    }
    return jwt.encode(data, _get_secret(), algorithm='HS256')


def _get_exp(t: int) -> str:
    return str(int(time.time()) + 60 * t)


def _get_secret() -> str:
    return 'secret'

