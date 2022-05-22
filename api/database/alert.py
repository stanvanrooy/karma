from .database import db


class Alert(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(10), nullable=False)
    labels = db.Column(db.JSON, nullable=False)
    annotations = db.Column(db.JSON, nullable=False)
    startsAt = db.Column(db.String(20), nullable=False)
    endsAt = db.Column(db.String(20), nullable=False)
    generatorURL = db.Column(db.String(100), nullable=False)
    webhook_id = db.Column(db.Integer, db.ForeignKey('webhook.id'), nullable=False)
    webhook = db.relationship('Webhook', backref=db.backref('alerts', lazy=True))

