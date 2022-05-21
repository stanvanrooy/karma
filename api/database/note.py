from .database import db

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    alert_id = db.Column(db.Integer, db.ForeignKey('alert.id'), nullable=False)
    alert = db.relationship('Alert', backref=db.backref('notes', lazy=True))
    text = db.Column(db.String(1024), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.now())

