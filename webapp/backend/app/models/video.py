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
from app import db
from app.models.mixins import TimestampMixin
from app.models.files import File
from app.models.source_channels import SourceChannel


class YoutubeVideo(TimestampMixin, db.Model):
    __tablename__ = 'youtube_videos'

    id = db.Column(db.Integer, primary_key=True)
    yt_id = db.Column(db.String, nullable=False)
    channel_id = db.Column(db.Integer, db.ForeignKey('source_channels.id'), nullable=False)
    channel = db.relationship('SourceChannel', backref=db.backref('videos', lazy=True), lazy='joined')
    title = db.Column(db.String, nullable=False)
    uri = db.Column(db.String, nullable=False)
    yt_published = db.Column(db.DateTime, nullable=False)
    yt_updated = db.Column(db.DateTime, nullable=False)

    @classmethod
    def from_xml(cls, xml):
        channel = SourceChannel.query.filter_by(channel_id=xml['yt:channelId']).first()
        return YoutubeVideo(
            yt_id=xml['yt:videoId'],
            channel=channel,
            title=xml['title'],
            uri=xml['link']['@href'],
            yt_published=xml['published'],
            yt_updated=xml['updated'],
        )

    def to_json(self):
        return {
            'id': self.id,
            'yt_id': self.yt_id,
            'channel_id': self.channel_id,
            'title': self.title,
            'uri': self.uri,
            'yt_published': self.yt_published,
            'yt_updated': self.yt_updated,
        }


class RecordTag(db.Model):
    __tablename__ = 'record_tags'

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String, nullable=False)
    record_id = db.Column(db.Integer, db.ForeignKey('records.id'), nullable=False)
    record = db.relationship('Record', backref=db.backref('tags', lazy=False), lazy='joined')


class Record(TimestampMixin, db.Model):
    __tablename__ = 'records'

    id = db.Column(db.Integer, primary_key=True)
    youtube_video_id = db.Column(db.Integer, db.ForeignKey('youtube_videos.id'), nullable=False)
    youtube_video = db.relationship('YoutubeVideo', backref=db.backref('records', lazy=True), lazy='joined')
    title = db.Column(db.String, nullable=False)
    descriptions = db.Column(db.String, nullable=False)
    audio_id = db.Column(db.Integer, db.ForeignKey('files.id'), nullable=True)
    audio = db.relationship('File', foreign_keys=[audio_id], backref=db.backref('audio_records', lazy=True), lazy='joined')
    image_id = db.Column(db.Integer, db.ForeignKey('files.id'), nullable=True)
    image = db.relationship('File', foreign_keys=[image_id], backref=db.backref('image_records', lazy=True), lazy='joined')
