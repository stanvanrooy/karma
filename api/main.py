from flask import Flask, g, request, jsonify
from flask.wrappers import Response
from flask_cors import CORS
from common import get_db

import alert

app = Flask(__name__)
CORS(app)


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.post('/api/note')
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
    alert.initialize_routes(app)
    app.run(debug=False, host='localhost')

