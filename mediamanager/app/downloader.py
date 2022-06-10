from os import environ
from uuid import uuid4

from app import celery
from app.YoutubeDownloader import YoutubeDownloader
from app.objects.download_task import DownloadTask
from app.objects.entry import Entry, AudioFile, ImageFile


@celery.task
def download(task: DownloadTask):
    _download(task)


def _download(task: DownloadTask):
    yt = YoutubeDownloader(environ.get('DOWNLOAD_PATH', f'/tmp/{str(uuid4())}'))
    info, files = yt.download(task.url)

    audio = None
    if 'audio' in files:
        audio = AudioFile(
            uri=files['audio'],
        )

    _id = info['id']
    entry = Entry(
        id=_id,
        author=info['channel'],
        title=info['title'],
        description=info['description'],
        url=f'https://www.youtube.com/watch?v={_id}',
        audio=audio,
        image=ImageFile(
            uri=f'https://img.youtube.com/vi/{_id}/maxresdefault.jpg',
        ),
    )

    return entry
