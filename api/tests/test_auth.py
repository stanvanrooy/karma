import auth
import config
import uuid


def test_generate_access_token_returns_valid_token():
    """
    GIVEN a user
    WHEN generate_access_token is called
    THEN it should return a valid token
    """
    user = str(uuid.uuid4())
    token = auth.generate_access_token(user)
    assert auth.validate_access_token(token) == user


def test_generate_refresh_token_returns_valid_token():
    """
    GIVEN a user
    WHEN generate_refresh_token is called
    THEN it should return a valid token
    """
    user = str(uuid.uuid4())
    token = auth.generate_refresh_token(user)
    assert auth.validate_refresh_token(token) == user


def test_validate_access_token_returns_none_if_expired():
    """
    GIVEN a user
    WHEN validate_access_token is called
    THEN it should return None
    """
    user = str(uuid.uuid4())
    token = auth.jwt_._encode(user, 'access_token', -10)
    assert auth.validate_access_token(token) is None


def test_validate_refresh_token_returns_none_if_expired():
    """
    GIVEN a user
    WHEN validate_refresh_token is called
    THEN it should return None
    """
    user = str(uuid.uuid4())
    token = auth.jwt_._encode(user, 'refresh_token', -10)
    assert auth.validate_refresh_token(token) is None


def test_login_with_correct_password_works(app, client):
    """
    GIVEN a user
    WHEN login is called with correct password
    THEN it should return the user
    """
    c = config.get_config()

    username = 'admin'
    password = c.admin.password

    with app.app_context():
        response = _post_login(client, username, password)
        assert response.status_code == 200

        acess_token = response.json.get('access_token')
        refresh_token = response.json.get('refresh_token')

        assert acess_token is not None
        assert auth.validate_access_token(acess_token) == username

        assert refresh_token is not None
        assert auth.validate_refresh_token(refresh_token) == username


def test_login_with_incorrect_password_fails(app, client):
    """
    GIVEN a user
    WHEN login is called with incorrect password
    THEN it should return 401
    """
    username = 'admin'
    password = 'wrong_password'

    with app.app_context():
        response = _post_login(client, username, password)
        assert response.status_code == 200
        assert response.json is None


def _post_login(client, username, password):
    return client.post('/api/1/auth/login', json={
        'username': username,
        'password': password
    })
