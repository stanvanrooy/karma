from flask import request, jsonify, Flask
from flask.wrappers import Response
from common import get_db
import models


def _get_key_value_pairs(d: dict):
    return [f"{k}={v}" for k, v in d.items()]


def _parse_key_value_pairs(s: str):
    return dict(kv.split("=") for kv in s.split(","))


def _replace_status(status: str):
    if status == 'resolved':
        return 'in-review'
    return status


def _add_alert():
    data: models.Webhook = request.get_json()
    db = get_db()
    for alert in data['alerts']:
        db.execute("""INSERT INTO 
            alerts (status, labels, annotations, startsAt, endsAt, generatorUrl) 
            VALUES (?, ?, ?, ?, ?, ?)""", (
            _replace_status(alert['status']), 
            ','.join(_get_key_value_pairs(alert['labels'])),
            ','.join(_get_key_value_pairs(alert['annotations'])),
            alert['startsAt'],
            alert['endsAt'],
            alert.get('generatorUrl') or alert.get('generatorURL')
        ));
    db.commit()

    return Response(status=200)


def _get_alerts():
    skip = int(request.args.get('skip', 0))
    limit = int(request.args.get('limit', 10))
    query = request.args.get('query', '').split(' ')
    db = get_db()
    
    queryQuery = [];
    for q in query:
        if q.startswith('status='):
            v = q.split('=')[1]
            queryQuery.append(f"WHERE status LIKE '{v}%'")
        else:
            queryQuery.append(f"WHERE labels LIKE '%{q}%'")

    queryQuery = 'AND \n'.join(queryQuery)
    alerts = db.execute(f"""SELECT * FROM alerts 
                        {queryQuery}
                        ORDER BY id DESC LIMIT ? OFFSET ?
                        """, (limit, skip)).fetchall()

    ret = []
    for alert in alerts:
        ret.append({
            'id': alert[0],
            'status': alert[1],
            'labels': _parse_key_value_pairs(alert[2]),
            'annotations': _parse_key_value_pairs(alert[3]),
            'startsAt': alert[4],
            'endsAt': alert[5],
            'generatorUrl': alert[6]
        })
    return jsonify(ret)


def _get_alert_count():
    db = get_db()
    count = db.execute("SELECT COUNT(*) FROM alerts").fetchone()[0]
    return jsonify({'count': count})


def _get_alert(id):
    db = get_db()
    alert = db.execute("SELECT * FROM alerts WHERE id = ?", (id,)).fetchone()
    if alert is None:
        return Response(status=404)

    return jsonify({
        'id': alert[0],
        'status': alert[1],
        'labels': _parse_key_value_pairs(alert[2]),
        'annotations': _parse_key_value_pairs(alert[3]),
        'startsAt': alert[4],
        'endsAt': alert[5],
        'generatorUrl': alert[6]
    })


def _delete_alert(id):
    db = get_db()
    db.execute("DELETE FROM alerts WHERE id = ?", (id,))
    db.commit()
    return Response(status=200)


def _update_alert(id):
    data: models.Alert = request.get_json()
    db = get_db()
    db.execute("""UPDATE alerts SET 
        status = ?, 
        labels = ?, 
        annotations = ?, 
        startsAt = ?, 
        endsAt = ?,
        generatorUrl = ?
        WHERE id = ?
    """, (
        data['status'], 
        ','.join(_get_key_value_pairs(data['labels'])),
        ','.join(_get_key_value_pairs(data['annotations'])),
        data['startsAt'],
        data['endsAt'],
        data['generatorUrl'],
        id
    ))
    db.commit()
    return jsonify(data)


def initialize_routes(app: Flask):
    app.route('/api/alert', methods=['POST'])(_add_alert)
    app.route('/api/alert', methods=['GET'])(_get_alerts)
    app.route('/api/alert/count', methods=['GET'])(_get_alert_count)
    app.route('/api/alert/<int:id>', methods=['GET'])(_get_alert)
    app.route('/api/alert/<int:id>', methods=['DELETE'])(_delete_alert)
    app.route('/api/alert/<int:id>', methods=['PUT'])(_update_alert)


