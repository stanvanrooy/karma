from flask import request, jsonify, Blueprint
import database
from . import common


n = Blueprint('notes', __name__)


@n.route('/', methods=['POST'])
@common.require_login()
def add_note():
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


@n.route('/', methods=['GET'])
@common.require_login()
def get_notes():
    skip = int(request.args.get('skip', 0))
    limit = int(request.args.get('limit', 10))
    notes = database.db.session.query(database.Note).offset(skip).limit(limit).all()
    return jsonify(notes)

