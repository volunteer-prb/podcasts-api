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
    """
    Download youtube audio by video link and place info to database.
    Check source channel id and task channel id

    Returns:
        Entry video
    """
    yt = YoutubeDownloader(environ.get('DOWNLOAD_PATH', f'/tmp/{str(uuid4())}'))
    # First download only meta information, such like channel id
    info, files = yt.download(task.url, download=False)

    _channel_id = info['channel_id']
    if _channel_id != task.channel_id:
        raise Exception(f'Entry channel id {_channel_id} does not match task channel id {task.channel_id}')

    # Second download files and meta information
    info, files = yt.download(task.url)

    audio = None
    if 'audio' in files:
        audio = AudioFile(
            uri=files['audio'],
        )

    _id = info['id']
    entry = Entry(
        id=_id,
        channel_id=info['channel_id'],
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
