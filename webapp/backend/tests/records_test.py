from datetime import datetime

import pytest

from flask_migrate import init, migrate, upgrade

from app import create_app, db
from app.celery import celery as _celery, publisher as _publisher
from app.models.files import AudioFile, File, FileUriType
from app.models.output_services import TelegramOutputService
from app.models.source_channels import SourceChannel, SourceChannelOutputService
from app.models.video import YoutubeVideo, Record


@pytest.fixture(scope='module')
def celery(request):
    _celery.conf.update(broker_url='memory://localhost/', task_always_eager=True)
    return _celery


@pytest.fixture(scope='module')
def publisher(request):
    _publisher.conf.update(broker_url='memory://localhost/', task_always_eager=True)
    return _publisher


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
        output_service = TelegramOutputService(title='Популярная политика',
                                               channel_id=-1000000000000,
                                               )
        source_channel = SourceChannel(title='Популярная политика',
                                          channel_id='UC7Elc-kLydl-NAV4g204pDQ',
                                          pubsubhubbub_mode='subscribe',
                                          )
        video = YoutubeVideo(
            yt_id='KBOny-tYdNQ',
            channel=source_channel,
            title='Ходорковский о конце Путина',
            uri='https://www.youtube.com/watch?v=KBOny-tYdNQ',
            yt_published=datetime.now(),
            yt_updated=datetime.now(),
        )
        record = Record(
            youtube_video=video,
            title='Ходорковский о конце Путина',
            descriptions='@descriptions',
            audio=AudioFile(
                uri='@uri',
                uri_type=FileUriType.file,
                duration_secs=58,
            ),
            image=File(
                uri='https://img.youtube.com/vi/KBOny-tYdNQ/maxresdefault.jpg',
                uri_type=FileUriType.global_link,
            ),
        )
        db.session.add_all([
            source_channel,
            output_service,
            SourceChannelOutputService(output_service=output_service,
                                       source_channel=source_channel,
                                       ),
            video,
            record
        ])
        db.session.commit()

    # other setup can go here

    yield app

    # clean up / reset resources here


@pytest.fixture()
def client(app, celery, publisher):
    return app.test_client()


def test_publish(client):
    resp = client.post('/records/publish/1')
    assert resp.status_code == 200
    assert resp.json['status'] == 'success'
    assert resp.json['data']['task_id']
