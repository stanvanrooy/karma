from flask import request, jsonify, Blueprint
from flask.wrappers import Response
import database
from . import common


a = Blueprint('alert', __name__)


@a.route('/', methods=['GET'])
@common.require_login()
def get_alerts():
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


@a.route('/count', methods=['GET'])
@common.require_login()
def get_alert_count():
    return jsonify({
        'count': database.db.session.query(database.Alert).count()
    })


@a.route('/<int:id>', methods=['GET'])
@common.require_login()
def get_alert(id):
    alert = database.db.session.query(database.Alert).filter(database.Alert.id == id).first()
    if alert is None:
        return Response(status=404)

    return jsonify(alert)


@a.route('/<int:id>', methods=['DELETE'])
@common.require_login()
def delete_alert(id):
    alert = database.db.session.query(database.Alert).filter(database.Alert.id == id).first()
    if alert is None:
        return Response(status=404)
    database.db.session.delete(alert)
    database.db.session.commit()
    return Response(status=200)


@a.route('/<int:id>', methods=['PUT'])
@common.require_login()
def update_alert(id):
    alert = database.db.session.query(database.Alert).filter(database.Alert.id == id).first()
    if alert is None:
        return Response(status=404)

    data = request.get_json()
    alert.update(**data)
    database.db.session.commit()
    return jsonify(alert)


@a.route('/api/alert/<int:id>/notes', methods=['GET'])
@common.require_login()
def get_alert_notes(id):
    notes = database.db.session.query(database.Note).filter(database.Note.alert_id == id).all()
    return jsonify(notes)
