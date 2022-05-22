from sqlalchemy.dialects.postgresql import UUID
from .database import db
import uuid

class Webhook(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(80), unique=True, nullable=False)

