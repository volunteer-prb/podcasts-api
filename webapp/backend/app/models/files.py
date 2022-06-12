import enum

from app import db
from app.models.mixins import TimestampMixin


class FileUriType(enum.Enum):
    file = 0  # mean that file can be direct read by mediamanager, backend, local telegram bot api server or nginx
    local_link = 1  # mean that file can be downloaded by URL, but access not allowed from global Internet
    global_link = 2  # mean that file can be downloaded by URL from anywhere


class File(TimestampMixin, db.Model):
    __tablename__ = 'files'

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String, nullable=False)
    # file path or URL
    uri = db.Column(db.String, nullable=False)
    # type of uri
    uri_type = db.Column(db.Enum(FileUriType), nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': 'file',
        'polymorphic_on': type,
    }


class AudioFile(File):
    __tablename__ = 'audio_files'

    id = db.Column(db.Integer, db.ForeignKey('files.id'), primary_key=True)
    duration_secs = db.Column(db.Integer, nullable=True)

    __mapper_args__ = {
        'polymorphic_identity': 'audio_file',
    }
