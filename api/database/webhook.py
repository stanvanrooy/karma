from sqlalchemy.dialects.postgresql import UUID
from .database import db
import uuid
from .base import Base

class Webhook(Base):
    name = db.Column(db.String(80), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name
        }
