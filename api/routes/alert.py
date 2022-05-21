from flask import request, jsonify, Flask
from flask.wrappers import Response
import database


def _add_alert():
    data = request.get_json()
    database.db.session.add(database.Alert(
        **data,
    ))
    database.db.session.commit()
    return Response(status=200)


def _get_alerts():
    skip = int(request.args.get('skip', 0))
    limit = int(request.args.get('limit', 10))
    query = request.args.get('query', '').split(' ')

    query = database.db.session.query(database.Alert)

    for q in query:
        if q.startswith('status='):
            v = q.split('=')[1]
            query = query.filter(database.Alert.status.like(v))
        else:
            query = query.filter(database.Alert.labels.like(q))

    alerts = query.order_by(database.Alert.startsAt.desc()).offset(skip).limit(limit).all()
    return jsonify(alerts)


def _get_alert_count():
    return jsonify({
        'count': database.db.session.query(database.Alert).count()
    })


def _get_alert(id):
    alert = database.db.session.query(database.Alert).filter(database.Alert.id == id).first()
    if alert is None:
        return Response(status=404)

    return jsonify(alert)


def _delete_alert(id):
    alert = database.db.session.query(database.Alert).filter(database.Alert.id == id).first()
    if alert is None:
        return Response(status=404)
    database.db.session.delete(alert)
    database.db.session.commit()
    return Response(status=200)


def _update_alert(id):
    alert = database.db.session.query(database.Alert).filter(database.Alert.id == id).first()
    if alert is None:
        return Response(status=404)

    data = request.get_json()
    alert.update(**data)
    database.db.session.commit()
    return jsonify(alert)


def initialize_routes(app: Flask):
    app.route('/api/alert', methods=['POST'])(_add_alert)
    app.route('/api/alert', methods=['GET'])(_get_alerts)
    app.route('/api/alert/count', methods=['GET'])(_get_alert_count)
    app.route('/api/alert/<int:id>', methods=['GET'])(_get_alert)
    app.route('/api/alert/<int:id>', methods=['DELETE'])(_delete_alert)
    app.route('/api/alert/<int:id>', methods=['PUT'])(_update_alert)

