import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
import auth


@pytest.fixture()
def app():
    from main import create_app
    app = create_app(True)
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

    yield app


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def ac(app):
    with app.app_context():
        token = auth.generate_access_token('admin')
        client = app.test_client()

        _put = client.put
        _post = client.post
        _get = client.get
        _patch = client.patch
        _delete = client.delete

        def post(*args, **kwargs):
            existing_headers = kwargs.get('headers', {})
            existing_headers['Authorization'] = f'Bearer {token}'
            kwargs['headers'] = existing_headers
            return _post(*args, **kwargs)

        def put(*args, **kwargs):
            existing_headers = kwargs.get('headers', {})
            existing_headers['Authorization'] = f'Bearer {token}'
            kwargs['headers'] = existing_headers
            return _put(*args, **kwargs)

        def get(*args, **kwargs):
            existing_headers = kwargs.get('headers', {})
            existing_headers['Authorization'] = f'Bearer {token}'
            kwargs['headers'] = existing_headers
            return _get(*args, **kwargs)

        def patch(*args, **kwargs):
            existing_headers = kwargs.get('headers', {})
            existing_headers['Authorization'] = f'Bearer {token}'
            kwargs['headers'] = existing_headers
            return _patch(*args, **kwargs)

        def delete(*args, **kwargs):
            existing_headers = kwargs.get('headers', {})
            existing_headers['Authorization'] = f'Bearer {token}'
            kwargs['headers'] = existing_headers
            return _delete(*args, **kwargs)

        client.post = post
        client.put = put
        client.get = get
        client.patch = patch
        client.delete = delete
        return client
