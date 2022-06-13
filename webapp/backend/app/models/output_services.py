import flask_sqlalchemy_extension as ext

from app import db
from app.models.mixins import TimestampMixin


class OutputService(TimestampMixin, ext.SerializeMixin, ext.DeserializeMixin, ext.QueryMixin, db.Model):
    __tablename__ = 'output_services'

    # inner DB primary key
    id = db.Column(db.Integer, primary_key=True)
    # type of output service (e.g. telegram, soundcloud)
    type = db.Column(db.String, nullable=False)
    # output service title
    title = db.Column(db.String, nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': 'general',
        'polymorphic_on': type,
    }


class TelegramOutputService(OutputService):
    __tablename__ = 'output_services_telegram'

    id = db.Column(db.Integer, db.ForeignKey('output_services.id'), primary_key=True)
    channel_id = db.Column(db.BigInteger, nullable=True)

    __mapper_args__ = {
        'polymorphic_identity': 'telegram',
    }
