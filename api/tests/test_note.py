import common

def test_add_note_anonymous_returns_401(client):
    response = client.post('/api/1/note', json={'text': 'test'})
    assert response.status_code == 401


def test_add_note_adds_note(app, ac):
    with app.app_context():
        alert = common.create_alert()

        response = ac.post('/api/1/note', json={
            'text': 'test',
            'alertId': alert.id
        })
        assert response.status_code == 200
        assert response.json['text'] == 'test'
