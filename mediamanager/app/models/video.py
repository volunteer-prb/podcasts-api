"""
<entry>
    <id>yt:video:VIDEO_ID</id>
    <yt:videoId>VIDEO_ID</yt:videoId>
    <yt:channelId>CHANNEL_ID</yt:channelId>
    <title>Video title</title>
    <link rel="alternate" href="http://www.youtube.com/watch?v=VIDEO_ID"/>
    <author>
        <name>Channel title</name>
        <uri>http://www.youtube.com/channel/CHANNEL_ID</uri>
    </author>
    <published>2015-03-06T21:40:57+00:00</published>
    <updated>2015-03-09T19:05:24.552394234+00:00</updated>
</entry>
"""
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship, backref

from app.models import Base
from app.models.mixins import TimestampMixin


class YoutubeVideo(TimestampMixin, Base):
    __tablename__ = 'youtube_videos'

    id = Column(Integer, primary_key=True)
    yt_id = Column(String, nullable=False)
    channel_id = Column(Integer, ForeignKey('source_channels.id'), nullable=False)
    channel = relationship('SourceChannel', backref=backref('videos', lazy=True), lazy='joined')
    title = Column(String, nullable=False)
    uri = Column(String, nullable=False)
    yt_published = Column(DateTime, nullable=False)
    yt_updated = Column(DateTime, nullable=False)


class RecordTag(Base):
    __tablename__ = 'record_tags'

    id = Column(Integer, primary_key=True)
    text = Column(String, nullable=False)
    record_id = Column(Integer, ForeignKey('records.id'), nullable=False)
    record = relationship('Record', backref=backref('tags', lazy=False), lazy='joined')


class Record(TimestampMixin, Base):
    __tablename__ = 'records'

    id = Column(Integer, primary_key=True)
    youtube_video_id = Column(Integer, ForeignKey('youtube_videos.id'), nullable=False)
    youtube_video = relationship('YoutubeVideo', backref=backref('records', lazy=True), lazy='joined')
    title = Column(String, nullable=False)
    descriptions = Column(String, nullable=False)
    audio_id = Column(Integer, ForeignKey('files.id'), nullable=True)
    audio = relationship('File', foreign_keys=[audio_id], backref=backref('audio_records', lazy=True), lazy='joined')
    image_id = Column(Integer, ForeignKey('files.id'), nullable=True)
    image = relationship('File', foreign_keys=[image_id], backref=backref('image_records', lazy=True), lazy='joined')
