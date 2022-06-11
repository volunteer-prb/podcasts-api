from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime

from app.models import Base
from app.models.mixins import TimestampMixin


class SourceChannel(TimestampMixin, Base):
    __tablename__ = 'source_channel'

    # inner primary key
    id = Column(Integer, primary_key=True)
    # youtube channel title
    title = Column(String, nullable=False)
    # youtube channel ID (part of URL)
    channel_id = Column(String, nullable=False)
    # youtube channel url
    uri = Column(String, nullable=True)
    # mode subscribe or unsubscribe
    pubsubhubbub_mode = Column(String, nullable=False)
    # subscribe expires date (need to refresh before expire)
    pubsubhubbub_expires_at = Column(DateTime, default=datetime.utcnow, nullable=False)
