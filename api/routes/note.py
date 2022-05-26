from flask import request, jsonify, Blueprint
import database
from . import common


n = Blueprint('notes', __name__)


@n.route('', methods=['POST'])
@common.require_login()
def add_note():
    data = request.get_json()
    if data is None:
        return jsonify({'error': 'No data received'}), 400

    if 'alertId' not in data or 'text' not in data:
        return jsonify({'error': 'Missing required field'}), 400

    note = database.Note(
        alert_id=data['alertId'],
        text=data['text']
    )

    database.db.session.add(note)
    database.db.session.commit()
    return jsonify(data)
