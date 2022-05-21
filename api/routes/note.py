from flask import request, jsonify, Flask
import database


def _add_note():
    data = request.get_json()
    if data is None:
        return jsonify({'error': 'No data received'}), 400

    if 'alertId' not in data or 'text' not in data:
        return jsonify({'error': 'Missing required field'}), 400

    note = database.Note(
        alertId=data['alertId'],
        text=data['text']
    )

    database.db.session.add(note)
    database.db.session.commit()
    return jsonify(data)


def _get_notes():
    skip = int(request.args.get('skip', 0))
    limit = int(request.args.get('limit', 10))
    notes = database.db.session.query(database.Note).offset(skip).limit(limit).all()
    return jsonify(notes)


def _get_alert_notes(id):
    notes = database.db.session.query(database.Note).filter_by(alertId=id).all()
    return jsonify(notes)


def initalize_routes(app: Flask):
    app.route('/notes', methods=['POST'])(_add_note)
    app.route('/notes', methods=['GET'])(_get_notes)
    app.route('/notes/alert/<id>', methods=['GET'])(_get_alert_notes)

