from os import environ

from flask import Blueprint

from app.celery import pubsubhubbub

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return 'Index'


@main.route('/list')
def profile():
    return 'List'


@main.route('//<string:channel_id>')
def test(channel_id: str):
    pubsubhubbub.subscribe.delay(channel_id, f'{environ.get("BASE_URL", "http://localhost")}/hooks/new/{channel_id}')
    return 'Test'
