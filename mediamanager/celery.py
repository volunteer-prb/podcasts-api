from celery import Celery
from mediamanager.objects.video import Entry

broker_url = 'amqp://guest@localhost:8080//'

celery = Celery('mediamanager', broker=broker_url)
celery.conf.update(
    task_serializer='json',
    # accept_content=['json'],  # Ignore other content
    result_serializer='json',
    timezone='Europe/Paris',
    enable_utc=True,
    result_persistent=True,
    ignore_result=False
)


def _download(video: Entry):
    print('Downloading {}'.format(video.title))
    return True


@celery.task
def download(video: Entry):
    _download(video)
