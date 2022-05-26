from .database import db
from .base import Base


class Alert(Base):
    status = db.Column(db.String(10), nullable=False)
    labels = db.Column(db.JSON, nullable=False)
    annotations = db.Column(db.JSON, nullable=False)
    startsAt = db.Column(db.String(20), nullable=False)
    endsAt = db.Column(db.String(20), nullable=False)
    generatorURL = db.Column(db.String(100), nullable=False)
    webhook_id = db.Column(db.Integer, db.ForeignKey('webhook.id'), nullable=False)
    webhook = db.relationship('Webhook', backref=db.backref('alerts', lazy=True))

    def to_dict(self):
        return {
            'id': self.id,
            'status': self.status,
            'labels': self.labels,
            'annotations': self.annotations,
            'startsAt': self.startsAt,
            'endsAt': self.endsAt,
            'generatorURL': self.generatorURL,
            'webhook_id': self.webhook_id
        }
