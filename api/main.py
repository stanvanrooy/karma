from flask import Flask, g, request, Response, jsonify
from flask_cors import CORS
import sqlite3

import constants
import models

app = Flask(__name__)
CORS(app)


def get_key_value_pairs(d: dict):
    return [f"{k}={v}" for k, v in d.items()]


def parse_key_value_pairs(s: str):
    return dict(kv.split("=") for kv in s.split(","))


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
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.post('/alert')
def hello_world():
    data: models.Webhook = request.get_json()
    db = get_db()
    for alert in data['alerts']:
        if alert['status'] == 'firing':
            continue
        db.execute("""INSERT INTO 
            alerts (status, labels, annotations, startsAt, endsAt, generatorURL) 
            VALUES (?, ?, ?, ?, ?, ?)""", (
            alert['status'], 
            ','.join(get_key_value_pairs(alert['labels'])),
            ','.join(get_key_value_pairs(alert['annotations'])),
            alert['startsAt'],
            alert['endsAt'],
            alert['generatorURL']
        ));
    db.commit()

    return Response(status=200)

@app.get('/alert')
def get_alerts():
    skip = int(request.args.get('skip', 0))
    limit = int(request.args.get('limit', 10))

    db = get_db()
    alerts = db.execute("SELECT * FROM alerts ORDER BY id DESC LIMIT ? OFFSET ?", (limit, skip)).fetchall()

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


@app.get('/alert/count')
def get_alert_count():
    db = get_db()
    count = db.execute("SELECT COUNT(*) FROM alerts").fetchone()[0]
    return jsonify({'count': count})


if __name__ == '__main__':
    app.run(debug=True)

