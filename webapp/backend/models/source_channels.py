from webapp.backend import db
from webapp.backend.models.mixins import TimestampMixin


class SourceChannels(TimestampMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    channel_id = db.Column(db.String, nullable=False)
    pubsubhubbub_mode = db.Column(db.String, nullable=False)
    pubsubhubbub_expires_at = db.Column(db.DateTime, nullable=False)
