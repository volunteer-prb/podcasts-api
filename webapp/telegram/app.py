from os import environ

from celery import Celery

app = Celery('telegram', broker=environ.get('TELEGRAM_BROKER', 'pyamqp://guest@localhost//'))


@app.task
def publish(envelope):
    """Publish envelope to telegram channels"""
    pass
