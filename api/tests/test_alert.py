import database
import common

def test_get_alerts_anonymous_returns_401(client):
    """
    GIVEN a request to /alert
    WHEN the request is not authenticated
    THEN check that the response is 401
    """
    response = client.get('/api/1/alert')
    assert response.status_code == 401


def test_get_alerts_returns_alerts(app, ac):
    with app.app_context():
        common.create_alert()
        response = ac.get('/api/1/alert')
        assert response.status_code == 200
        assert len(response.json) != 0


def test_get_alert_anonymous_returns_401(client):
    """
    GIVEN a request to /alert
    WHEN the request is not authenticated
    THEN check that the response is 401
    """
    response = client.get('/api/1/alert/1')
    assert response.status_code == 401


def test_get_alert_returns_alert(app, ac):
    with app.app_context():
        alert = common.create_alert()
        response = ac.get('/api/1/alert/{}'.format(alert.id))
        assert response.status_code == 200
        assert response.json['id'] == alert.id


def test_get_alert_count_anyone_returns_401(client):
    """
    GIVEN a request to /alert/count
    WHEN the request is not authenticated
    THEN check that the response is 401
    """
    response = client.get('/api/1/alert/count')
    assert response.status_code == 401


def test_get_alert_count_returns_count(app, ac):
    with app.app_context():
        count = database.db.session.query(database.Alert).count()
        response = ac.get('/api/1/alert/count')
        assert response.status_code == 200
        assert response.json['count'] == count


def test_delete_alert_anonymous_returns_401(client):
    """
    GIVEN a request to /alert
    WHEN the request is not authenticated
    THEN check that the response is 401
    """
    response = client.delete('/api/1/alert/1')
    assert response.status_code == 401


def test_delete_alert_deletes_alert(app, ac):
    with app.app_context():
        alert = common.create_alert()
        response = ac.delete('/api/1/alert/{}'.format(alert.id))
        assert response.status_code == 200
        database.db.session.query(database.Alert).get(alert.id) is None


def test_update_alert_anonymous_returns_401(client):
    """
    GIVEN a request to /alert
    WHEN the request is not authenticated
    THEN check that the response is 401
    """
    response = client.put('/api/1/alert/1')
    assert response.status_code == 401


def test_update_alert_updates_alert(app, ac):
    with app.app_context():
        alert = common.create_alert()
        response = ac.put('/api/1/alert/{}'.format(alert.id), json={
            'status': 'resolved',
            'endsAt': '2019-01-01T00:00:00Z'
        })
        assert response.status_code == 200
        assert response.json['status'] == 'resolved'
        assert response.json['endsAt'] == '2019-01-01T00:00:00Z'


def test_get_alert_notes_anonymous_returns_401(client):
    """
    GIVEN a request to /alert/notes
    WHEN the request is not authenticated
    THEN check that the response is 401
    """
    response = client.get('/api/1/alert/1/notes')
    assert response.status_code == 401


def test_get_alert_notes_returns_notes(app, ac):
    with app.app_context():
        alert = common.create_alert()
        common.create_note(alert)
        response = ac.get('/api/1/alert/{}/notes'.format(alert.id))
        assert response.status_code == 200
        assert len(response.json) == 1
        assert response.json[0]['text'] == 'Test note'
