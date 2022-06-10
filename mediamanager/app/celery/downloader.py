from app.celery import celery
from app.objects.video import Entry


@celery.task
def download(video: Entry):
    _download(video)


def _download(video: Entry):
    print('Downloading {}'.format(video.title))
    return True
