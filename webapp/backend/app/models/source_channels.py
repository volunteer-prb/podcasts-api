from datetime import datetime

import flask_sqlalchemy_extension as ext

from app import db
from app.models.mixins import TimestampMixin


class SourceChannel(TimestampMixin, ext.SerializeMixin, ext.DeserializeMixin, ext.QueryMixin, db.Model):
    __tablename__ = 'source_channels'

    # inner DB primary key
    id = db.Column(db.Integer, primary_key=True)
    # youtube channel title
    title = db.Column(db.String, nullable=False)
    # youtube channel ID (part of URL)
    channel_id = db.Column(db.String, nullable=False)
    # youtube channel url
    uri = db.Column(db.String, nullable=True)
    # mode subscribe or unsubscribe
    pubsubhubbub_mode = db.Column(db.String, nullable=False)
    # subscribe expires date (need to refresh before expire)
    pubsubhubbub_expires_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    # pubsubhubbub verify token, used only in subscribe/unsubscribe event
    verify_token = db.Column(db.String, nullable=False)


class SourceChannelOutputService(ext.SerializeMixin, db.Model):
    __tablename__ = 'source_channels_to_output_services'

    id = db.Column(db.Integer, primary_key=True)

    output_service_id = db.Column(db.Integer, db.ForeignKey('output_services.id'), nullable=False)
    output_service = db.relationship('OutputService', backref=db.backref('sources', lazy=True), lazy='joined')

    source_channel_id = db.Column(db.Integer, db.ForeignKey('source_channels.id'), nullable=False)
    source_channel = db.relationship('SourceChannel', backref=db.backref('outputs', lazy=True), lazy='joined')
