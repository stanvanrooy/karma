from flask import Blueprint, request, jsonify
from . import common
import database


w = Blueprint('webhook', __name__)


@w.route('/<string:id>', methods=['POST'])
def add_alert(id):
    webhook = database.db.session.query(database.Webhook).filter_by(id=id).first()
    if webhook is None:
        return '', 400

    data = request.get_json()
    database.db.session.add(database.Alert(
        **data,
        webhook_id=webhook.id
    ))
    database.db.session.commit()
    return '', 200


@w.route('/', methods=['POST'])
def add_webhook():
    data = request.get_json()
    if data is None:
        return 'No data provided', 400

    webhook = database.Webhook(
        name=data.get('name', 'Default'),
    )
    database.db.session.add(webhook)
    database.db.session.commit()
    return jsonify(webhook)
