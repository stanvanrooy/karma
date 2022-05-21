from flask import request, jsonify, Flask
from common import get_db


def _add_note():
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


def _get_notes():
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

def _get_alert_notes(id):
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


def initalize_routes(app: Flask):
    app.route('/notes', methods=['POST'])(_add_note)
    app.route('/notes', methods=['GET'])(_get_notes)
    app.route('/notes/alert/<id>', methods=['GET'])(_get_alert_notes)


