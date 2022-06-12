import enum

from sqlalchemy import Column, Integer, String, Enum, ForeignKey

from app.models import Base
from app.models.mixins import TimestampMixin


class FileUriType(enum.Enum):
    file = 0  # mean that file can be direct read by mediamanager, backend, local telegram bot api server or nginx
    local_link = 1  # mean that file can be downloaded by URL, but access not allowed from global Internet
    global_link = 2  # mean that file can be downloaded by URL from anywhere


class File(TimestampMixin, Base):
    __tablename__ = 'files'

    id = Column(Integer, primary_key=True)
    type = Column(String, nullable=False)
    # file path or URL
    uri = Column(String, nullable=False)
    # type of uri
    uri_type = Column(Enum(FileUriType), nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': 'file',
        'polymorphic_on': type,
    }


class AudioFile(File):
    __tablename__ = 'audio_files'

    id = Column(Integer, ForeignKey('files.id'), primary_key=True)
    duration_secs = Column(Integer, nullable=True)

    __mapper_args__ = {
        'polymorphic_identity': 'audio_file',
    }
