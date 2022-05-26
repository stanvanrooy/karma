from flask import Blueprint, request, jsonify
from . import common
import database
import logging


w = Blueprint('webhook', __name__)


@w.route('/<string:id>', methods=['POST'])
def add_alert(id):
    webhook = database.db.session.query(database.Webhook).filter_by(id=id).first()
    if webhook is None:
        logging.info('bad request - webhook not found')
        return '', 400

    data = request.get_json()
    database.db.session.add(database.Alert(
        **data,
        webhook_id=webhook.id
    ))
    database.db.session.commit()
    return '', 200


@w.route('', methods=['POST'])
@common.require_login()
def add_webhook():
    data = request.get_json()
    if data is None:
        logging.info('bad request - no data')
        return 'No data provided', 400

    webhook = database.Webhook(
        name=data.get('name', 'Default'),
    )
    database.db.session.add(webhook)
    database.db.session.commit()
    return jsonify(webhook.to_dict()), 201


@w.route('', methods=['GET'])
@common.require_login()
def get_webhooks():
    skip = int(request.args.get('skip', 0))
    limit = int(request.args.get('limit', 10))
    
    webhooks = database.db.session.query(database.Webhook).offset(skip).limit(limit).all()
    return jsonify([webhook.to_dict() for webhook in webhooks]), 200


@w.route('/count', methods=['GET'])
@common.require_login()
def get_webhook_count():
    count = database.db.session.query(database.Webhook).count()
    return jsonify({'count': count})


@w.route('/<string:id>', methods=['DELETE'])
@common.require_login()
def delete_webhook(id):
    webhook = database.db.session.query(database.Webhook).filter_by(id=id).first()
    if webhook is None:
        logging.info('bad request - webhook not found')
        return '', 400

    database.db.session.delete(webhook)
    database.db.session.commit()
    return jsonify(webhook.to_dict())

