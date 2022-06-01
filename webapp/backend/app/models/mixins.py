from datetime import datetime

from app import db


class TimestampMixin:
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated = db.Column(db.DateTime, onupdate=datetime.utcnow, default=datetime.utcnow)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
