from flask import Blueprint, request, jsonify
import auth
import database
import logging


a = Blueprint('auth', __name__)


@a.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if data is None:
        return "No data", 400

    if 'username' not in data or 'password' not in data:
        return "Missing required field", 400

    username = data['username']
    password = data['password']

    user = database.db.session.query(database.User).filter_by(username=username).first()
    if user is None:
        logging.info('login rejected: %s - user not found', username)
        return "Invalid user/password combination", 200

    valid_credentials = auth.verify_password(user.password, password)
    if not valid_credentials:
        logging.info('login rejected: %s - invalid credentials', username)
        return "Invalid user/password combination", 200

    token, refresh_token = _generate_tokens(username)
    return jsonify({'token': token, 'refresh_token': refresh_token})


def _generate_tokens(username: str):
    access_token = auth.generate_access_token(username)
    refresh_token = auth.generate_refresh_token(username)
    return access_token, refresh_token

