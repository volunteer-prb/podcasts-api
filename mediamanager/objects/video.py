'''
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
'''


class Entry:

    def __init__(self, json):
        self.id = json['id']
        self.videoId = json['yt:videoId']
        self.channelId = json['yt:channelId']
        self.title = json['title']
        self.link = json['link']['@href']
        self.author = json['author']['name']
        self.uri = json['author']['uri']
        self.published = json['published']
        self.updated = json['updated']

    def to_json(self):
        return {
            'id': self.id,
            'videoId': self.videoId,
            'channelId': self.channelId,
            'title': self.title,
            'link': self.link,
            'author': self.author,
            'uri': self.uri,
            'published': self.published,
            'updated': self.updated
        }
