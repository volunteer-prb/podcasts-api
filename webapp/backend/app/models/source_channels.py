from app import db
from app.models.mixins import TimestampMixin


class SourceChannel(TimestampMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    channel_id = db.Column(db.String, nullable=False)
    pubsubhubbub_mode = db.Column(db.String, nullable=False)
    pubsubhubbub_expires_at = db.Column(db.DateTime, nullable=False)

    def to_json(self):
        return {
            'id': self.id,
            'channel_id': self.channel_id,
            'pubsubhubbub_mode': self.pubsubhubbub_mode,
            'pubsubhubbub_expires_at': self.pubsubhubbub_expires_at.timestamp()
        }
