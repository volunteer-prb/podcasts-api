from datetime import datetime

import flask_sqlalchemy_extension.model as ext

from app import db
from app.models.mixins import TimestampMixin


class SourceChannel(TimestampMixin, ext.SerializeMixin, ext.DeserializeMixin, ext.QueryMixin, db.Model):
    # inner DB primary key
    id = db.Column(db.Integer, primary_key=True)
    # youtube channel title
    title = db.Column(db.String, nullable=False)
    # youtube channel ID (part of URL)
    channel_id = db.Column(db.String, nullable=False)
    # mode subscribe or unsubscribe
    pubsubhubbub_mode = db.Column(db.String, nullable=False)
    # subscribe expires date (need to refresh before expire)
    pubsubhubbub_expires_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
