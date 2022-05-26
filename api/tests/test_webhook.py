import database
import common

def test_add_webhook_anonymous_returns_401(client):
    response = client.post('/api/1/webhook', json={})
    assert response.status_code == 401


def test_add_webhook_adds_webhook(app, ac):
    with app.app_context():
        response = ac.post('/api/1/webhook', json={
            'name': 'test',
        })
        assert response.status_code == 201
        webhook = database.db.session.query(database.Webhook).get(response.json['id'])
        assert webhook.name == 'test'


def test_get_webhooks_anonymous_returns_401(client):
    response = client.get('/api/1/webhook')
    assert response.status_code == 401


def test_get_webhooks_returns_webhooks(app, ac):
    with app.app_context():
        common.create_webhook()
        response = ac.get('/api/1/webhook')
        assert response.status_code == 200
        assert len(response.json) != 0
