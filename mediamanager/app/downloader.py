from datetime import datetime
from os import environ
from uuid import uuid4

from sqlalchemy.orm import Session

from app import celery
from app.YoutubeDownloader import YoutubeDownloader
from app.models import db
from app.models.files import FileUriType
from app.models.source_channels import SourceChannel
from app.models.video import YoutubeVideo, Record, RecordTag
from app.objects.download_task import DownloadTask
from app.objects.entry import Entry, AudioFile, ImageFile, Channel


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
            duration=info['duration'],
        )

    _id = info['id']
    entry = Entry(
        id=_id,
        channel=Channel(
            id=info['channel_id'],
            title=info['channel'],
            url=info['channel_url'],
        ),
        title=info['title'],
        description=info['description'],
        url=info['webpage_url'],
        tags=info['tags'],
        audio=audio,
        image=ImageFile(
            uri=f'https://img.youtube.com/vi/{_id}/maxresdefault.jpg',
        ),
    )

    _save_entry(entry)

    return entry


def _save_entry(entry: Entry):
    """
    Query channel (by channel_id) and video (by yt_id) from database,
    update video information from entry, save updates
    """
    with Session(db) as session:
        channel = session.query(SourceChannel).filter_by(channel_id=entry.channel.id).first()
        if not channel:
            raise Exception(f'Source channel {entry.channel.id} does not found in database')

        # Try query video from database by Youtube ID, if does not found create new
        video = session.query(YoutubeVideo).filter_by(yt_id=entry.id, channel=channel).first()

        if not video:
            video = YoutubeVideo(
                yt_id=entry.id,
                title=entry.title,
                channel=channel,
                uri=entry.url,
                yt_published=datetime.now(),  # yt_dlp does not provide this information
                yt_updated=datetime.now(),  # yt_dlp does not provide this information
            )
            session.add(video)

        from app.models import files

        # Save record information
        audio = None
        if entry.audio:
            audio = files.AudioFile(
                uri=entry.audio.uri,
                uri_type=FileUriType.file,
                duration_secs=entry.audio.duration,
            )

        record = Record(
            youtube_video=video,
            title=entry.title,
            descriptions=entry.description,
            audio=audio,
            image=files.File(
                uri=entry.image.uri,
                uri_type=FileUriType.global_link,
            ),
        )
        for _tag in entry.tags:
            tag = RecordTag(
                text=_tag,
                record=record,
            )
            session.add(tag)

        session.add(record)
        session.commit()
