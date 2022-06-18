from unittest.mock import patch

import pytest

from flask_migrate import init, migrate, upgrade

from app import create_app, db
from app.celery import media_manager as _media_manager, celery as _celery
from app.celery.pubsubhubbub import generate_signature
from app.models.source_channels import SourceChannel

xml_example = '''<feed xmlns:yt="http://www.youtube.com/xml/schemas/2015"
         xmlns="http://www.w3.org/2005/Atom">
                <link rel="hub" href="https://pubsubhubbub.appspot.com"/>
                <link rel="self" href="https://www.youtube.com/xml/feeds/videos.xml?channel_id=CHANNEL_ID"/>
                <title>YouTube video feed</title>
                <updated>2015-04-01T19:05:24.552394234+00:00</updated>
                <entry>
                    <id>yt:video:VIDEO_ID</id>
                    <yt:videoId>VIDEO_ID_PYTEST</yt:videoId>
                    <yt:channelId>pytest_channel_sub_id</yt:channelId>
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
def media_manager(request):
    _media_manager.conf.update(broker_url='memory://localhost/', task_always_eager=True)
    return _media_manager


@pytest.fixture(scope='module')
def celery(request):
    _celery.conf.update(broker_url='memory://localhost/', task_always_eager=True)
    return _celery


@pytest.fixture()
def app(tmpdir):
    _tmpdir = str(tmpdir)
    db_connection = f'sqlite:///{_tmpdir}/test-db.sqlite'
    migrations_dir = f'{_tmpdir}/migrations'
    # migrations_dir = f'../migrations'

    app = create_app()
    app.config.update({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': db_connection
    })

    # create new clear database for tests

    with app.app_context():
        init(migrations_dir)
        migrate(migrations_dir, 'init')
        upgrade(migrations_dir)

        # create data for tests
        channel_subscribe = SourceChannel(
            title='test subscribe',
            channel_id='pytest_channel_sub_id',
            pubsubhubbub_mode='subscribe',
            verify_token='QWEQWE',
            secret='QWE-QWE',
        )
        channel_unsubscribe = SourceChannel(
            title='test unsubscribe',
            channel_id='pytest_channel_unsub_id',
            pubsubhubbub_mode='unsubscribe',
            verify_token='EWQEWQ',
            secret='EWQ-EWQ',
        )
        db.session.add(channel_subscribe)
        db.session.add(channel_unsubscribe)
        db.session.commit()

    # other setup can go here

    yield app

    # clean up / reset resources here


@pytest.fixture()
def client(app, media_manager):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()


def test_hooks(client):
    _sign = generate_signature(xml_example.encode('utf8'), 'QWE-QWE')
    headers = {
        'X-Hub-Signature': f'sha1={_sign}',
    }
    resp = client.post('/hooks/new/pytest_channel_sub_id', data=xml_example, headers=headers)
    assert resp.status_code == 200
    assert resp.is_json is True
    assert resp.json['status'] == 'success'
    assert resp.json['data']['yt_id'] == 'VIDEO_ID_PYTEST'


def test_hooks_invalid_secret(client):
    _sign = generate_signature(xml_example.encode('utf8'), 'INVALID_KEY')
    headers = {
        'X-Hub-Signature': f'sha1={_sign}',
    }
    resp = client.post('/hooks/new/pytest_channel_sub_id', data=xml_example, headers=headers)
    assert resp.status_code == 200
    assert resp.is_json is True
    assert resp.json['status'] == 'success'
    assert not resp.json['data']  # empty data


@pytest.mark.parametrize("channel_id, status_code", [
    ('pytest_channel_unsub_id', 400),
    ('pytest_channel_notfound_id', 404),
])
def test_hooks_error_channel(client, channel_id, status_code):
    # valid key for invalid channel,
    # in real it could not be happens, but if it happened
    _sign = generate_signature(xml_example.encode('utf8'), 'EWQ-EWQ')
    headers = {
        'X-Hub-Signature': f'sha1={_sign}',
    }
    resp = client.post(f'/hooks/new/{channel_id}', data=xml_example, headers=headers)
    assert resp.status_code == status_code


@pytest.mark.parametrize("mode, channel_id, verify_token", [
    ('subscribe', 'pytest_channel_sub_id', 'QWEQWE'),
    ('unsubscribe', 'pytest_channel_unsub_id', 'EWQEWQ'),
])
def test_hook_subscribe_good(client, mode, channel_id, verify_token):
    resp = client.get(f'/hooks/new/{channel_id}', query_string={
        'hub.lease_seconds': 4000,
        'hub.mode': mode,
        'hub.challenge': 'qwerty',
        'hub.verify_token': verify_token,
    })
    assert resp.status_code == 200
    assert resp.data == b'qwerty'


@pytest.mark.parametrize("status_code, mode, channel_id, lease_seconds, verify_token", [
    (404, 'subscribe', 'pytest_channel_notfound_id', 100, 'QWEQWE'),
    (400, 'unsubscribe', 'pytest_channel_unsub_id', None, 'QWEQWE'),
    (204, 'subscribe', 'pytest_channel_unsub_id', 100, 'QWEQWE'),
    (204, 'subscribe', 'pytest_channel_sub_id', 100, 'EWQEWQ'),
])
def test_hook_subscribe_error(client, status_code, mode, channel_id, lease_seconds, verify_token):
    resp = client.get(f'/hooks/new/{channel_id}', query_string={
        'hub.lease_seconds': lease_seconds,
        'hub.mode': mode,
        'hub.challenge': 'qwerty',
        'hub.verify_token': verify_token,
    })
    assert resp.status_code == status_code
