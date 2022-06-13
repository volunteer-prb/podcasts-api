import os.path
from datetime import datetime, timedelta

import pytest
from sqlalchemy.orm import Session

from app.downloader import _save_entry, _download
from app.models import db, Base
from app.models.source_channels import SourceChannel
from app.models.video import Record, YoutubeVideo
from app.objects.download_task import DownloadTask
from app.objects.entry import Entry, Channel, AudioFile, ImageFile


@pytest.fixture()
def session():
    Base.metadata.create_all(bind=db)
    _session = Session(db)
    channel = SourceChannel(
        title='Exist channel',
        channel_id='UC7Elc-kLydl-NAV4g204pDQ',
        pubsubhubbub_mode='subscribe',
        pubsubhubbub_expires_at=datetime.now() + timedelta(days=30),
    )
    _session.add_all([channel])
    _session.commit()
    return _session


@pytest.fixture()
def entry_example():
    return Entry(
        id='qwerty',
        title='@title',
        description='@description',
        url='https://youtube.com/#url',
        tags=['hello', 'world'],
        channel=Channel(
            id='UC7Elc-kLydl-NAV4g204pDQ',
            title='Channel title',
            url='https://youtube.com/#channel_url',
        ),
        audio=AudioFile(
            uri='https://example.com/audio.mp3',
            duration=2022,
        ),
        image=ImageFile(
            uri='https://example.com/image.jpg',
        ),
    )


@pytest.fixture()
def download_task_example():
    return DownloadTask(
        url='https://www.youtube.com/shorts/KBOny-tYdNQ',
        channel_id='UC7Elc-kLydl-NAV4g204pDQ',
    )


@pytest.fixture()
def download_task_example2():
    return DownloadTask(
        url='https://www.youtube.com/watch?v=QH-IEtw0EjM',
        channel_id='UCgxTPTFbIbCWfTR9I2-5SeQ',
    )


def test_select_channel(session):
    with session:
        should_exist = session.query(SourceChannel).filter_by(channel_id='UC7Elc-kLydl-NAV4g204pDQ').first()
        assert should_exist
        assert should_exist.channel_id == 'UC7Elc-kLydl-NAV4g204pDQ'


def test_save_entry(session, entry_example):
    _save_entry(entry_example)

    with session:
        youtube_video = session.query(YoutubeVideo).filter_by(yt_id=entry_example.id).first()
        assert youtube_video
        video = session.query(Record).filter_by(youtube_video=youtube_video).first()
        assert video
        assert len(video.tags) == 2


def test_download(session, download_task_example):
    entry = _download(download_task_example)
    assert entry
    assert os.path.exists(entry.audio.uri)

    with session:
        youtube_video = session.query(YoutubeVideo).filter_by(yt_id=entry.id).first()
        assert youtube_video
        video = session.query(Record).filter_by(youtube_video=youtube_video).first()
        assert video
        assert video.tags
        assert video.audio.duration_secs == 58


def test_download_fail_channel_mismatch(session, download_task_example):
    download_task_example.channel_id = 'not-match-channel_id'
    with pytest.raises(Exception):
        entry = _download(download_task_example)


def test_download_fail_channel_does_not_exists(session, download_task_example2):
    with pytest.raises(Exception):
        entry = _download(download_task_example2)


def test_download_fail_video_miss(session, download_task_example):
    download_task_example.url = 'https://www.youtube.com/watch?v=qwerty'
    from yt_dlp import DownloadError
    with pytest.raises(DownloadError):
        entry = _download(download_task_example)
