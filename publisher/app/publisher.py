from app import celery
from app.objects.Envelope import Envelope
from app.telegram import publisher


@celery.task()
def publish(data):
    """Publish envelope (topic) to social media by recipients list"""
    envelope = Envelope.from_json(data)
    publisher.publish(envelope)
