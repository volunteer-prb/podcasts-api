from datetime import datetime

from sqlalchemy import Column, DateTime


class TimestampMixin:
    created = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated = Column(DateTime, onupdate=datetime.utcnow, default=datetime.utcnow)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
