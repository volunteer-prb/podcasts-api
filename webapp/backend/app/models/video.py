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


class YoutubeVideo(TimestampMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    yt_id = db.Column(db.String, nullable=False)
    channel_id = db.Column(db.Integer, db.ForeignKey('source_channel.id'), nullable=False)
    channel = db.relationship('SourceChannel', backref=db.backref('videos', lazy=True), lazy='joined')
    title = db.Column(db.String, nullable=False)
    link = db.Column(db.String, nullable=False)
    author = db.Column(db.String, nullable=False)
    uri = db.Column(db.String, nullable=False)
    yt_published = db.Column(db.DateTime, nullable=False)
    yt_updated = db.Column(db.DateTime, nullable=False)

    @classmethod
    def from_xml(cls, xml):
        return YoutubeVideo(
            yt_id=xml['yt:videoId'],
            channel_id=xml['yt:channelId'],
            title=xml['title'],
            link=xml['link']['@href'],
            author=xml['author']['name'],
            uri=xml['author']['uri'],
            yt_published=xml['published'],
            yt_updated=xml['updated'],
        )

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
