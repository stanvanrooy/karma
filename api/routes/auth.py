from flask import Flask, request, jsonify
import auth
import common


def _login():
    data = request.get_json()
    if data is None:
        return "No data", 400
    if 'username' not in data or 'password' not in data:
        return "Invalid user/password combination", 200

    username = data['username']
    password = data['password']

    db = common.get_db()
    user = db.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()

    valid_credentials = auth.verify_password(user.password, password)
    if not valid_credentials:
        return "Invalid user/password combination", 200

    token, refresh_token = _generate_tokens(username)
    return jsonify({'token': token, 'refresh_token': refresh_token})


def _generate_tokens(username: str):
    access_token = auth.generate_access_token(username)
    refresh_token = auth.generate_refresh_token(username)
    return access_token, refresh_token


def initialize_routes(app: Flask):
    app.route('/login', methods=['POST'])(_login)

