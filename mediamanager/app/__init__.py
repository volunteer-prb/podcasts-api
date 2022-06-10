from celery import Celery
from kombu.serialization import register

from app.objects import serializer

register(
    'json',
    serializer.dumps,
    serializer.loads,
    content_type='application/json',
)
celery = Celery('media_manager', broker='redis://')
