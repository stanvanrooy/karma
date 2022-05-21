from flask import Flask, g, request, Response, jsonify
from flask_cors import CORS
from functools import wraps
import sqlite3

import constants
import models

app = Flask(__name__)
CORS(app)


def get_key_value_pairs(d: dict):
    return [f"{k}={v}" for k, v in d.items()]


def parse_key_value_pairs(s: str):
    return dict(kv.split("=") for kv in s.split(","))


def replace_status(status: str):
    if status == 'resolved':
        return 'in-review'
    return status


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(constants.DATABASE)
        try:
            db.execute("""CREATE TABLE alerts (
                id INTEGER PRIMARY KEY AUTOINCREMENT, 
                status TEXT, 
                labels TEXT, 
                annotations TEXT, 
                startsAt datetime, 
                endsAt datetime,
                generatorUrl TEXT
            )""")
        except:
            pass
        try:
            db.execute("""CREATE TABLE notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT, 
                alertId INTEGER, 
                text TEXT, 
                createdAt datetime DEFAULT (datetime('now','localtime'))
            )""")
        except:
            pass
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


def authenticate():
    def _authenticate(f):
        @wraps(f)
        def __authenticate(*args, **kwargs):
            if request.headers.get('Authorization') != constants.AUTH_TOKEN:
                return Response(status=401)
            return f(*args, **kwargs)
        return __authenticate
    return _authenticate


@app.post('/api/alert')
@authenticate()
def add_alert():
    data: models.Webhook = request.get_json()
    db = get_db()
    for alert in data['alerts']:
        db.execute("""INSERT INTO 
            alerts (status, labels, annotations, startsAt, endsAt, generatorUrl) 
            VALUES (?, ?, ?, ?, ?, ?)""", (
            replace_status(alert['status']), 
            ','.join(get_key_value_pairs(alert['labels'])),
            ','.join(get_key_value_pairs(alert['annotations'])),
            alert['startsAt'],
            alert['endsAt'],
            alert.get('generatorUrl') or alert.get('generatorURL')
        ));
    db.commit()

    return Response(status=200)


@app.get('/api/alert')
@authenticate()
def get_alerts():
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
            'labels': parse_key_value_pairs(alert[2]),
            'annotations': parse_key_value_pairs(alert[3]),
            'startsAt': alert[4],
            'endsAt': alert[5],
            'generatorUrl': alert[6]
        })
    return jsonify(ret)


@app.get('/api/alert/count')
@authenticate()
def get_alert_count():
    db = get_db()
    count = db.execute("SELECT COUNT(*) FROM alerts").fetchone()[0]
    return jsonify({'count': count})


@app.get('/api/alert/<id>')
@authenticate()
def get_alert(id):
    db = get_db()
    alert = db.execute("SELECT * FROM alerts WHERE id = ?", (id,)).fetchone()
    if alert is None:
        return Response(status=404)

    return jsonify({
        'id': alert[0],
        'status': alert[1],
        'labels': parse_key_value_pairs(alert[2]),
        'annotations': parse_key_value_pairs(alert[3]),
        'startsAt': alert[4],
        'endsAt': alert[5],
        'generatorUrl': alert[6]
    })


@app.delete('/api/alert/<id>')
@authenticate()
def delete_alert(id):
    db = get_db()
    db.execute("DELETE FROM alerts WHERE id = ?", (id,))
    db.commit()
    return Response(status=200)


@app.put('/api/alert/<id>')
@authenticate()
def update_alert(id):
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
        ','.join(get_key_value_pairs(data['labels'])),
        ','.join(get_key_value_pairs(data['annotations'])),
        data['startsAt'],
        data['endsAt'],
        data['generatorUrl'],
        id
    ))
    db.commit()
    return jsonify(data)


@app.post('/api/note')
@authenticate()
def add_note():
    data = request.get_json()
    db = get_db()
    db.execute("""INSERT INTO 
        notes (alertId, text) 
        VALUES (?, ?)""", (
        data['alertId'],
        data['text'],
    ))
    db.commit()
    return jsonify(data)


@app.get('/api/note')
@authenticate()
def get_notes():
    skip = int(request.args.get('skip', 0))
    limit = int(request.args.get('limit', 10))
    db = get_db()
    notes = db.execute("SELECT * FROM notes ORDER BY id DESC LIMIT ? OFFSET ?", (limit, skip)).fetchall()

    ret = []
    for note in notes:
        ret.append({
            'id': note[0],
            'alertId': note[1],
            'text': note[2],
            'createdAt': note[3]
        })
    return jsonify(ret)

@app.get('/api/alert/<id>/notes')
@authenticate()
def get_alert_notes(id):
    db = get_db()
    notes = db.execute("SELECT * FROM notes WHERE alertId = ? ORDER BY id", (id, )).fetchall()

    ret = []
    for note in notes:
        ret.append({
            'id': note[0],
            'alertId': note[1],
            'text': note[2],
            'createdAt': note[3]
        })
    return jsonify(ret)


if __name__ == '__main__':
    app.run(debug=False, host='localhost')

