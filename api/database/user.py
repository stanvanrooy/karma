from .database import db
from .base import Base

class User(Base):
    username = db.Column(db.String(80), unique=True, nullable=False, primary_key=True)
    password = db.Column(db.String(256), nullable=False)

