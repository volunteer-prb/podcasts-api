import pytest

from flask_migrate import init, migrate, upgrade

from app import create_app, db
from app.celery import celery as _celery
from app.models.source_channels import SourceChannel


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
        channel_subscribe = SourceChannel(title='test subscribe',
                                          channel_id='pytest_channel_sub_id',
                                          pubsubhubbub_mode='subscribe',
                                          )
        channel_unsubscribe = SourceChannel(title='test unsubscribe',
                                            channel_id='pytest_channel_unsub_id',
                                            pubsubhubbub_mode='unsubscribe',
                                            )
        db.session.add(channel_subscribe)
        db.session.add(channel_unsubscribe)
        db.session.commit()

    # other setup can go here

    yield app

    # clean up / reset resources here


@pytest.fixture()
def client(app, celery):
    return app.test_client()


@pytest.mark.parametrize("filter, expected_length", [('%', 2),
                                                     ('%unsub%', 1),
                                                     ('notfound', 0),
                                                     ])
def test_find(client, filter, expected_length):
    resp = client.get('/channels/find', query_string={
        'filter_by_title__ilike': filter,
    })
    assert resp.status_code == 200
    assert resp.json['status'] == 'success'
    assert resp.json['data']['pagination']['page'] == 1
    assert len(resp.json['data']['items']) == expected_length


@pytest.mark.parametrize("_id, expected_title", [(1, 'test subscribe'),
                                                 (2, 'test unsubscribe'),
                                                 ])
def test_get(client, _id, expected_title):
    resp = client.get(f'/channels/{_id}')
    assert resp.status_code == 200
    assert resp.json['status'] == 'success'
    assert resp.json['data']['id'] == _id
    assert resp.json['data']['title'] == expected_title


def test_get_notfound(client):
    resp = client.get(f'/channels/100')
    assert resp.status_code == 404
    assert resp.json['status'] == 'error'


def test_post(client):
    resp = client.post('/channels/', json=dict(
        title='test post',
        channel_id='pytest_channel_post_id',
        pubsubhubbub_mode='subscribe',
    ))
    assert resp.status_code == 200
    assert resp.json['status'] == 'success'
    assert resp.json['data']['title'] == 'test post'


def test_post_error(client):
    resp = client.post('/channels/', json=dict(
        title='test post',
        channel_id='pytest_channel_post_id',
    ))
    assert resp.status_code == 500
    assert resp.json['status'] == 'error'
    assert resp.json['message'] == 'Column `pubsubhubbub_mode` must have not null value'


def test_put(client):
    resp = client.put('/channels/1', json=dict(
        title='test put',
    ))
    assert resp.status_code == 200
    assert resp.json['status'] == 'success'
    assert resp.json['data']['title'] == 'test put'
    assert resp.json['data']['channel_id'] == 'pytest_channel_sub_id'


def test_put_error(client):
    resp = client.put('/channels/100', json=dict(
        title='test put error',
    ))
    assert resp.status_code == 404
    assert resp.json['status'] == 'error'


def test_delete(client):
    resp = client.delete('/channels/2')
    assert resp.status_code == 200
    assert resp.json['status'] == 'success'


def test_delete_error(client):
    resp = client.delete('/channels/100')
    assert resp.status_code == 404
    assert resp.json['status'] == 'error'

