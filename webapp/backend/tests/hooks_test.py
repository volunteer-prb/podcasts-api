import pytest
from app import create_app
from mediamanager.celery import celery

xml_examp = '''<feed xmlns:yt="http://www.youtube.com/xml/schemas/2015"
         xmlns="http://www.w3.org/2005/Atom">
                <link rel="hub" href="https://pubsubhubbub.appspot.com"/>
                <link rel="self" href="https://www.youtube.com/xml/feeds/videos.xml?channel_id=CHANNEL_ID"/>
                <title>YouTube video feed</title>
                <updated>2015-04-01T19:05:24.552394234+00:00</updated>
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
                </feed>'''


@pytest.fixture(scope='module')
def celery_app(request):
    celery.conf.update(task_always_eager=True)
    return celery


@pytest.fixture()
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
    })

    # other setup can go here

    yield app

    # clean up / reset resources here


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()


def test_hooks(client, celery_app):
    resp = client.post('/hooks/new', data=xml_examp)
    assert resp.status_code == 200
    assert resp.is_json is True
    assert resp.json['id'] == 'yt:video:VIDEO_ID'
