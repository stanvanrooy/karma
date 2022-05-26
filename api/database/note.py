from .database import db
from .base import Base

class Note(Base):
    alert_id = db.Column(db.Integer, db.ForeignKey('alert.id'), nullable=False)
    alert = db.relationship('Alert', backref=db.backref('notes', lazy=True))
    text = db.Column(db.String(1024), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.now())

    def to_dict(self):
        return {
            'id': self.id,
            'alert_id': self.alert_id,
            'text': self.text,
            'created_at': self.created_at
        }

