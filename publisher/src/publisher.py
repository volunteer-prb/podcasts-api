from celery import Celery

from objects.Envelope import Envelope
from telegram import publisher

app = Celery('publisher', broker='redis://')


@app.task()
def publish(data):
    """Publish envelope (topic) to social media by recipients list"""
    envelope = Envelope.from_json(data)
    publisher.publish(envelope)
