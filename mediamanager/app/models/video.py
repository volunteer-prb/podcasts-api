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
    __tablename__ = 'youtube_video'

    id = Column(Integer, primary_key=True)
    yt_id = Column(String, nullable=False)
    channel_id = Column(Integer, ForeignKey('source_channel.id'), nullable=False)
    channel = relationship('SourceChannel', backref=backref('videos', lazy=True), lazy='joined')
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    uri = Column(String, nullable=False)
    yt_published = Column(DateTime, nullable=False)
    yt_updated = Column(DateTime, nullable=False)

    def to_json(self):
        return {
            'id': self.id,
            'yt_id': self.yt_id,
            'channel_id': self.channel_id,
            'title': self.title,
            'link': self.link,
            'author': self.author,
            'uri': self.uri,
            'yt_published': self.yt_published,
            'yt_updated': self.yt_updated,
        }
